from __future__ import annotations

import concurrent.futures
import json
import re
import sys
import threading
import time
from typing import Any

import requests

from config import settings
from scraper.tv_database import SeriesDatabase
from database.models import get_db_url
from sqlalchemy import text
from tmdb_service import _choose_best_match


# Regex patterns for cleaning titles (reuse from update_tmdb.py patterns)
YEAR_PATTERN = re.compile(r"\b((?:19|20)\d{2})\b")
NOISE_PATTERNS = [
    re.compile(r"\b(?:season|episode|ep|s\d{1,2}|e\d{1,2}|complete|series)\b", re.IGNORECASE),
    re.compile(r"\b(?:hdrip|webrip|web-dl|bluray|brrip|dvdrip|720p|1080p|2160p|4k)\b", re.IGNORECASE),
    re.compile(r"\b(?:x264|x265|h\.?264|h\.?265|hevc|aac|dual[- ]audio)\b", re.IGNORECASE),
    re.compile(r"\b(?:download|watch|new link|link)\b", re.IGNORECASE),
]


def _safe(text: str) -> str:
    """Return a console-safe version of *text* (handles Windows cp1252)."""
    return text.encode("ascii", errors="replace").decode("ascii")


def clean_title_and_extract_year(raw_title: str) -> tuple[str, int | None]:
    """Clean TV series titles before searching TMDB."""
    title = raw_title.strip()

    # Extract year
    years = YEAR_PATTERN.findall(title)
    year = None
    if years:
        year = int(years[-1])
        title = YEAR_PATTERN.sub(" ", title)

    # Clean noise patterns
    for pattern in NOISE_PATTERNS:
        title = pattern.sub(" ", title)

    # Split CamelCase
    title = re.sub(r'([a-z])([A-Z])', r'\1 \2', title)

    # Remove dots
    title = title.replace(".", " ")

    # Clean punctuation
    title = re.sub(r"[\_\-\:\/\|\\\*\+]", " ", title)
    title = re.sub(r"[\[\]{}()\"\'\`~!?@#\$%\^&;]", " ", title)

    # Normalize whitespace
    title = re.sub(r"\s+", " ", title).strip()

    return title, year


class TMDBTVClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.base_url = "https://api.themoviedb.org/3"
        self.request_lock = threading.Lock()

    def request(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        all_params = {"api_key": self.api_key, **params}

        max_retries = 5
        backoff = 1.0

        for attempt in range(max_retries):
            try:
                with self.request_lock:
                    time.sleep(0.05)

                response = self.session.get(url, params=all_params, timeout=15)

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    sleep_time = float(retry_after) if retry_after and retry_after.isdigit() else backoff
                    print(f"  [Rate Limited] Waiting {sleep_time}s on attempt {attempt+1}...")
                    time.sleep(sleep_time)
                    backoff *= 2
                    continue

                if response.status_code >= 500:
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as exc:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"TMDB request to {path} failed: {exc}") from exc
                time.sleep(backoff)
                backoff *= 2
                continue

        raise RuntimeError(f"TMDB request to {path} failed after {max_retries} retries")

    def search_tv(self, title: str, year: int | None = None) -> dict[str, Any] | None:
        query = title.strip()
        if not query:
            return None

        params = {
            "query": query,
            "include_adult": "false",
        }
        if year:
            params["first_air_date_year"] = str(year)

        try:
            response = self.request("/search/tv", params)
        except Exception:
            return None

        results = response.get("results", [])
        if not results:
            return None

        # Adapt for _choose_best_match compatibility
        for r in results:
            r["title"] = r.get("name", "")
            r["original_title"] = r.get("original_name", "")
            r["release_date"] = r.get("first_air_date", "")

        best_match = _choose_best_match(query, results, expected_year=year)
        return {
            "tmdb_id": best_match.get("id"),
            "name": best_match.get("name"),
            "original_name": best_match.get("original_name"),
            "first_air_date": best_match.get("first_air_date"),
        }

    def get_tv_details(self, tmdb_id: int) -> dict[str, Any]:
        response = self.request(f"/tv/{tmdb_id}", {})
        return {
            "poster_path": response.get("poster_path"),
            "backdrop_path": response.get("backdrop_path"),
            "overview": response.get("overview"),
            "vote_average": response.get("vote_average"),
            "number_of_seasons": response.get("number_of_seasons"),
            "number_of_episodes": response.get("number_of_episodes"),
            "genres": [genre["name"] for genre in response.get("genres", [])],
            "status": response.get("status"),
        }


class Stats:
    def __init__(self, total_to_process: int, already_linked: int):
        self.total_to_process = total_to_process
        self.already_linked = already_linked
        self.processed = 0
        self.matched = 0
        self.not_found = 0
        self.errors = 0
        self.lock = threading.Lock()

    def increment_processed(self) -> int:
        with self.lock:
            self.processed += 1
            return self.processed

    def increment_matched(self):
        with self.lock:
            self.matched += 1

    def increment_not_found(self):
        with self.lock:
            self.not_found += 1

    def increment_errors(self):
        with self.lock:
            self.errors += 1


def process_series(
    series: Any,
    client: TMDBTVClient,
    database: SeriesDatabase,
    stats: Stats,
    db_lock: threading.Lock,
) -> None:
    raw_title = series["title"]
    series_id = int(series["id"])

    cleaned_title, year = clean_title_and_extract_year(raw_title)
    year_str = str(year) if year else "N/A"

    idx = stats.increment_processed()
    remaining = stats.total_to_process - idx

    safe_raw = _safe(raw_title)
    safe_clean = _safe(cleaned_title)

    log_msg = f"[{idx}/{stats.total_to_process}] Processing: \"{safe_raw}\"\n"
    log_msg += f"  Cleaned: \"{safe_clean}\" | Year: {year_str}\n"

    try:
        tmdb_result = None
        if cleaned_title:
            tmdb_result = client.search_tv(cleaned_title, year=year)
            if not tmdb_result and year:
                log_msg += f"  (No match with year {year}; trying without year...)\n"
                tmdb_result = client.search_tv(cleaned_title)

        if not tmdb_result:
            stats.increment_not_found()
            log_msg += "  Matched: No (Not Found)\n"
            sys.stdout.write(log_msg + "\n")
            sys.stdout.flush()

            if idx % 50 == 0 or idx == stats.total_to_process:
                with stats.lock:
                    matched = stats.matched
                    not_found = stats.not_found
                    errors = stats.errors
                sys.stdout.write(f"--- Progress: {idx}/{stats.total_to_process} | Matched: {matched} | Not Found: {not_found} | Errors: {errors} | Remaining: {remaining} ---\n\n")
                sys.stdout.flush()
            return

        # Fetch details
        details = client.get_tv_details(int(tmdb_result["tmdb_id"]))
        tmdb_data = {
            **tmdb_result,
            **details,
        }

        # Save and link
        with db_lock:
            tmdb_tv_id = database.save_tmdb_tv(tmdb_data)
            database.link_series_to_tmdb(series_id, tmdb_tv_id)

        stats.increment_matched()
        safe_name = _safe(tmdb_result['name'])
        log_msg += f"  Matched: Yes -> \"{safe_name}\" (TMDB ID: {tmdb_result['tmdb_id']}, Air: {tmdb_result.get('first_air_date') or 'N/A'})\n"
        sys.stdout.write(log_msg + "\n")
        sys.stdout.flush()

    except Exception as exc:
        stats.increment_errors()
        log_msg += f"  Error: {exc}\n"
        sys.stdout.write(log_msg + "\n")
        sys.stdout.flush()

    if idx % 50 == 0 or idx == stats.total_to_process:
        with stats.lock:
            matched = stats.matched
            not_found = stats.not_found
            errors = stats.errors
        sys.stdout.write(f"--- Progress: {idx}/{stats.total_to_process} | Matched: {matched} | Not Found: {not_found} | Errors: {errors} | Remaining: {remaining} ---\n\n")
        sys.stdout.flush()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    db_url = get_db_url(settings.database_url, settings.database_path)
    database = SeriesDatabase(db_url)

    # Count already linked
    with database._connection() as session:
        already_linked_count = session.scalar(
            text("SELECT COUNT(*) FROM tv_series WHERE tmdb_tv_id IS NOT NULL")
        )
        total_count = session.scalar(text("SELECT COUNT(*) FROM tv_series"))

    to_process = database.get_series_without_tmdb()
    total_to_process = len(to_process)

    print("=" * 60)
    print("  TV SERIES TMDB UPDATER START")
    print("=" * 60)
    print(f"  Total series in DB       : {total_count}")
    print(f"  Already linked to TMDB   : {already_linked_count}")
    print(f"  Unlinked to process      : {total_to_process}")
    print(f"  Concurrency Level        : 4 Threads")
    print("=" * 60)
    print()

    tmdb_key = settings.tmdb_api_key
    if not tmdb_key:
        print("Error: Missing TMDB_API_KEY environment variable.")
        sys.exit(1)

    client = TMDBTVClient(tmdb_key)
    stats = Stats(total_to_process, already_linked_count)
    db_lock = threading.Lock()
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_series, s, client, database, stats, db_lock)
            for s in to_process
        ]
        concurrent.futures.wait(futures)

    elapsed = time.time() - start_time

    print("=" * 60)
    print("  TV SERIES TMDB UPDATE COMPLETE")
    print("=" * 60)
    print(f"  Total processed         : {stats.processed}")
    print(f"  Successfully matched    : {stats.matched}")
    print(f"  Not found               : {stats.not_found}")
    print(f"  Errors/Skipped          : {stats.errors}")
    print(f"  Already linked          : {already_linked_count}")
    print(f"  Total execution time    : {elapsed:.1f} seconds")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
