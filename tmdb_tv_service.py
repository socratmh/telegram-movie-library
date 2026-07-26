from __future__ import annotations

import re
from typing import Any

from tmdb_service import _tmdb_get, _choose_best_match


def search_tv(title: str, year: int | str | None = None) -> dict[str, Any] | None:
    """
    Search TMDB by TV series title and return the best matching result.

    Returned keys:
    - tmdb_id
    - name
    - original_name
    - first_air_date
    """
    query = title.strip()
    if not query:
        return None

    params = {
        "query": query,
        "include_adult": "false",
    }
    if year:
        params["first_air_date_year"] = str(year)

    response = _tmdb_get("/search/tv", params)
    results = response.get("results", [])
    if not results:
        return None

    # Adapt results so _choose_best_match can compare title fields
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


def get_tv_details(tmdb_id: int, language: str | None = None) -> dict[str, Any]:
    """
    Fetch detailed TMDB metadata for a TV series.

    Returned keys:
    - poster_path
    - backdrop_path
    - overview
    - vote_average
    - number_of_seasons
    - number_of_episodes
    - genres
    - status
    """
    params = {}
    if language:
        params["language"] = language
    response = _tmdb_get(f"/tv/{tmdb_id}", params)
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
