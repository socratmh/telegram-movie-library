"""
migrate_tv_channel_links.py — Migrate TV series Telegram links to a new channel.

When a Telegram channel gets banned or replaced, this script:
1. Updates the TVLibrary record with the new channel URL and numeric ID.
2. Scrapes the new channel for TV series messages.
3. Matches scraped messages to existing TVSeries records (by exact title, fuzzy title).
4. Replaces old telegram_channel_link values with updated message links.

Usage:
    python migrate_tv_channel_links.py --library-id 1 --new-channel "https://t.me/+XXXXX" --new-channel-id "1234567890"

Flags:
    --library-id        ID of the TV library to migrate (required)
    --new-channel       New Telegram channel URL or @handle (required)
    --new-channel-id    Numeric channel ID for private deep links (optional)
    --dry-run           Preview matches without writing to DB
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from dataclasses import dataclass, field

from rapidfuzz import fuzz
from sqlalchemy import select
from telethon import TelegramClient

from config import settings
from database.models import get_db_url, init_db
from database.tv_models import TVLibrary, TVSeries, TMDBTVSeries
from scraper.tv_parser import parse_series_message


# ---------------------------------------------------------------------------
# Matching engine
# ---------------------------------------------------------------------------

@dataclass
class MatchResult:
    series_id: int
    series_title: str
    new_message_id: int
    new_link: str
    scraped_title: str
    method: str          # "exact", "fuzzy"
    score: float = 1.0   # 0-100 for fuzzy, 1.0 for exact


@dataclass
class MigrationStats:
    total_scraped: int = 0
    matched_exact: int = 0
    matched_fuzzy: int = 0
    unmatched: int = 0
    unmatched_titles: list[str] = field(default_factory=list)


FUZZY_THRESHOLD = 80  # minimum fuzz ratio to accept


def build_match_indexes(session, library_id: int):
    """Build lookup structures from existing TV series in library."""
    series_list = session.execute(
        select(TVSeries, TMDBTVSeries)
        .outerjoin(TMDBTVSeries, TVSeries.tmdb_tv_id == TMDBTVSeries.id)
        .where(TVSeries.library_id == library_id)
    ).all()

    # title (lowered) -> series_id
    title_index: dict[str, int] = {}
    # tmdb_id -> series_id
    tmdb_index: dict[int, int] = {}
    # list of (series_id, title) for fuzzy
    fuzzy_candidates: list[tuple[int, str]] = []

    for series, tmdb in series_list:
        lower = series.title.strip().lower()
        title_index[lower] = series.id
        fuzzy_candidates.append((series.id, series.title))
        if tmdb and tmdb.tmdb_id:
            tmdb_index[tmdb.tmdb_id] = series.id

    return title_index, tmdb_index, fuzzy_candidates


def match_message(
    scraped_title: str,
    message_id: int,
    new_link: str,
    title_index: dict[str, int],
    tmdb_index: dict[int, int],
    fuzzy_candidates: list[tuple[int, str]],
    series_titles: dict[int, str],
) -> MatchResult | None:
    """Try to match a scraped series message to an existing TV series."""
    lower = scraped_title.strip().lower()

    # 1. Exact title match
    if lower in title_index:
        sid = title_index[lower]
        return MatchResult(
            series_id=sid,
            series_title=series_titles[sid],
            new_message_id=message_id,
            new_link=new_link,
            scraped_title=scraped_title,
            method="exact",
        )

    # 2. Fuzzy match
    best_score = 0.0
    best_id = None
    for sid, candidate_title in fuzzy_candidates:
        score = fuzz.ratio(lower, candidate_title.strip().lower())
        if score > best_score:
            best_score = score
            best_id = sid

    if best_id is not None and best_score >= FUZZY_THRESHOLD:
        return MatchResult(
            series_id=best_id,
            series_title=series_titles[best_id],
            new_message_id=message_id,
            new_link=new_link,
            scraped_title=scraped_title,
            method="fuzzy",
            score=best_score,
        )

    return None


# ---------------------------------------------------------------------------
# Main migration logic
# ---------------------------------------------------------------------------

def _safe(text: str) -> str:
    return text.encode("ascii", errors="replace").decode("ascii")


def _build_telegram_url(channel: str, message_id: int, resolved_channel_id: str | None) -> str:
    """Construct a direct Telegram link for a message in a channel."""
    clean_channel = channel.strip()
    if clean_channel.startswith("@"):
        return f"https://t.me/{clean_channel[1:]}/{message_id}"
    if "t.me/" in clean_channel and not clean_channel.startswith("https://t.me/+"):
        handle = clean_channel.split("t.me/")[-1].strip("/")
        if handle and not handle.startswith("+"):
            return f"https://t.me/{handle}/{message_id}"
    if resolved_channel_id:
        return f"https://t.me/c/{resolved_channel_id}/{message_id}"
    return clean_channel


async def migrate_tv(
    library_id: int,
    new_channel: str,
    new_channel_id: str | None,
    dry_run: bool,
) -> None:
    db_url = get_db_url(settings.database_url, settings.database_path)
    SessionLocal = init_db(db_url)

    with SessionLocal() as session:
        library = session.execute(
            select(TVLibrary).where(TVLibrary.id == library_id)
        ).scalar_one_or_none()
        if library is None:
            print(f"ERROR: TV Library with id={library_id} not found.")
            sys.exit(1)

        print(f"TV Library: {_safe(library.name)} (id={library.id})")
        print(f"  Old channel: {library.telegram_channel}")
        print(f"  New channel: {new_channel}")
        print()

        # Build match indexes
        title_index, tmdb_index, fuzzy_candidates = build_match_indexes(session, library_id)
        # series_id -> title for display
        series_titles = {sid: title for title, sid in [(t, s) for s, t in fuzzy_candidates]}

        print(f"Loaded {len(fuzzy_candidates)} existing TV series for matching.")
        print()

    # Scrape new channel
    print(f"Connecting to Telegram and scraping: {new_channel}")
    print("This may take a while for large channels...")
    print()

    client = TelegramClient(
        settings.telegram_session_name,
        settings.telegram_api_id,
        settings.telegram_api_hash,
    )
    await client.start()

    resolved_channel_id = new_channel_id
    scraped: list[tuple[str, int, str]] = []  # (title, message_id, link)
    count = 0
    try:
        # Auto-resolve channel entity to get ID
        try:
            entity = await client.get_entity(new_channel)
            entity_id_str = str(entity.id)
            if entity_id_str.startswith("-100"):
                entity_id_str = entity_id_str[4:]
            if not resolved_channel_id:
                resolved_channel_id = entity_id_str
            print(f"Auto-resolved channel ID from Telegram: {resolved_channel_id}")
        except Exception as e:
            print(f"Warning: Could not auto-resolve channel ID via Telethon: {e}")

        async for message in client.iter_messages(new_channel, limit=None):
            count += 1
            if count % 500 == 0:
                print(f"  ... scanned {count} messages ...")

            parsed = parse_series_message(message.message)
            if parsed and parsed.title:
                link = parsed.telegram_link or _build_telegram_url(new_channel, message.id, resolved_channel_id)
                scraped.append((parsed.title, message.id, link))
    finally:
        await client.disconnect()

    print(f"\nScraped {count} messages, found {len(scraped)} TV series candidates.")
    print()

    # Match
    stats = MigrationStats(total_scraped=len(scraped))
    matches: list[MatchResult] = []

    for scraped_title, msg_id, link in scraped:
        result = match_message(
            scraped_title, msg_id, link,
            title_index, tmdb_index, fuzzy_candidates, series_titles,
        )
        if result:
            matches.append(result)
            if result.method == "exact":
                stats.matched_exact += 1
            else:
                stats.matched_fuzzy += 1
        else:
            stats.unmatched += 1
            stats.unmatched_titles.append(scraped_title)

    # Print results
    print("=" * 60)
    print("  TV MATCHING RESULTS")
    print("=" * 60)
    print(f"  Total scraped series     : {stats.total_scraped}")
    print(f"  Matched (exact title)    : {stats.matched_exact}")
    print(f"  Matched (fuzzy)          : {stats.matched_fuzzy}")
    print(f"  Unmatched                : {stats.unmatched}")
    print("=" * 60)
    print()

    if stats.unmatched > 0:
        print("Unmatched titles (first 20):")
        for title in stats.unmatched_titles[:20]:
            print(f"  - {_safe(title)}")
        print()

    # Show some fuzzy matches for review
    fuzzy_matches = [m for m in matches if m.method == "fuzzy"]
    if fuzzy_matches:
        print("Fuzzy matches (review these):")
        for m in fuzzy_matches[:20]:
            print(f"  [{m.score:.0f}%] \"{_safe(m.scraped_title)}\" -> \"{_safe(m.series_title)}\"")
        print()

    if dry_run:
        print("DRY RUN — no database changes made.")
        return

    # Apply changes
    print("Applying changes to database...")
    with SessionLocal() as session:
        # 1. Update TV library record
        library = session.execute(
            select(TVLibrary).where(TVLibrary.id == library_id)
        ).scalar_one()

        library.telegram_channel = new_channel
        if new_channel_id:
            library.telegram_channel_id = new_channel_id
        elif resolved_channel_id:
            library.telegram_channel_id = resolved_channel_id

        # 2. Update TVSeries.telegram_channel_link for matched series
        updated_count = 0
        for m in matches:
            series = session.execute(
                select(TVSeries).where(TVSeries.id == m.series_id)
            ).scalar_one_or_none()
            if series:
                series.telegram_channel_link = m.new_link
                updated_count += 1

        session.commit()

    print(f"Done. Updated {updated_count} TV series links and library channel info.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Migrate TV series Telegram links to a new channel."
    )
    parser.add_argument(
        "--library-id", type=int, required=True,
        help="ID of the TV library to migrate",
    )
    parser.add_argument(
        "--new-channel", required=True,
        help="New Telegram channel URL or @handle",
    )
    parser.add_argument(
        "--new-channel-id", default=None,
        help="Numeric channel ID for private deep links (without -100 prefix)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview matches without writing to database",
    )
    args = parser.parse_args()

    asyncio.run(migrate_tv(
        library_id=args.library_id,
        new_channel=args.new_channel,
        new_channel_id=args.new_channel_id,
        dry_run=args.dry_run,
    ))


if __name__ == "__main__":
    main()
