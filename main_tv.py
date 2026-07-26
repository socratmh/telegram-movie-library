from __future__ import annotations

import asyncio
import os
import time

from config import settings
from scraper.tv_database import SeriesDatabase
from scraper.tv_scraper import TelegramSeriesScraper, SeriesScrapeStats
from scraper.telegram_client import get_telegram_client
from database.models import get_db_url


def _safe(text: str) -> str:
    """Return a console-safe version of *text* (handles Windows cp1252)."""
    return text.encode("ascii", errors="replace").decode("ascii")


async def run() -> None:
    db_url = get_db_url(settings.database_url, settings.database_path)

    # Read target library ID & Telegram channel from environment
    env_id = os.environ.get("LIBRARY_ID")
    library_id = int(env_id) if env_id else None
    tv_channel = os.environ.get("TELEGRAM_CHANNEL", "").strip() or os.environ.get("TV_SERIES_CHANNEL", "").strip()

    if not tv_channel:
        print("Error: TELEGRAM_CHANNEL or TV_SERIES_CHANNEL environment variable is not set.")
        return

    database = SeriesDatabase(db_url, library_id=library_id)

    # Load known titles for target library
    known_titles = database.get_known_titles()
    print(f"Library ID: {library_id or 'All'}")
    print(f"Found {len(known_titles)} existing TV series in the database.")
    print()

    stats = SeriesScrapeStats()
    start_time = time.time()

    async with get_telegram_client() as client:
        scraper = TelegramSeriesScraper(client, tv_channel)

        print(f"Scraping TV series channel: {tv_channel}")
        print("This may take a while for channels with many messages...")
        print()

        async for message in client.iter_messages(tv_channel, limit=None):
            stats.total_messages_scanned += 1

            if stats.total_messages_scanned % 200 == 0:
                print(f"  ... scanned {stats.total_messages_scanned} messages so far ...")

            record = scraper._parse_message(message)
            if not record:
                continue

            stats.total_series_found += 1

            if record.title in known_titles:
                stats.duplicates_skipped += 1
                continue

            # Save to database
            saved = database.save_series([record.to_dict()])
            if saved > 0:
                stats.new_series_added += 1
                known_titles.add(record.title)
                link_info = f", link: {record.telegram_link}" if record.telegram_link else ""
                print(f"  [NEW] {_safe(record.title)} (msg #{record.message_id}{link_info})")

    elapsed = time.time() - start_time

    # Final report
    print()
    print("=" * 60)
    print("  TV SERIES SCRAPING COMPLETE")
    print("=" * 60)
    print(f"  Total messages scanned  : {stats.total_messages_scanned}")
    print(f"  Total series found      : {stats.total_series_found}")
    print(f"  Duplicates skipped      : {stats.duplicates_skipped}")
    print(f"  New series added        : {stats.new_series_added}")
    print(f"  Time elapsed            : {elapsed:.1f}s")
    print("=" * 60)
    print()


if __name__ == "__main__":
    asyncio.run(run())
