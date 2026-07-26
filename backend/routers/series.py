"""TV Series API router — public endpoints for TV libraries and series."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from backend.tv_database import SeriesQueries
from backend.tv_models import (
    SeriesDetailResponse,
    SeriesGenreListResponse,
    SeriesPaginatedResponse,
    SeriesStatsResponse,
    TVLibraryListResponse,
    TVLibraryResponse,
)

router = APIRouter(prefix="/api", tags=["series"])


def _get_queries(request: Request) -> SeriesQueries:
    return request.app.state.series_queries  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# TV Library Endpoints
# ---------------------------------------------------------------------------

@router.get("/tv-libraries", response_model=TVLibraryListResponse)
def list_tv_libraries(
    queries: SeriesQueries = Depends(_get_queries),
) -> TVLibraryListResponse:
    """Return all active TV libraries with series counts."""
    return TVLibraryListResponse(libraries=queries.get_tv_libraries())


@router.get("/tv-libraries/{slug}", response_model=TVLibraryResponse)
def get_tv_library(
    slug: str,
    queries: SeriesQueries = Depends(_get_queries),
) -> TVLibraryResponse:
    """Return a single TV library by slug."""
    lib = queries.get_tv_library_by_slug(slug)
    if lib is None:
        raise HTTPException(status_code=404, detail="TV Library not found")
    return TVLibraryResponse(**lib)


# ---------------------------------------------------------------------------
# Series Endpoints
# ---------------------------------------------------------------------------

@router.get("/series", response_model=SeriesPaginatedResponse)
def list_series(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search series by title"),
    genre: str | None = Query(None, description="Filter by genre name"),
    sort_by: str = Query(
        "title",
        description="Sort field",
        pattern="^(title|first_air_date|vote_average)$",
    ),
    sort_order: str = Query(
        "asc",
        description="Sort direction",
        pattern="^(asc|desc)$",
    ),
    library_id: int | None = Query(None, description="Filter by TV library ID"),
    queries: SeriesQueries = Depends(_get_queries),
) -> SeriesPaginatedResponse:
    """Return a paginated list of TV series with lightweight TMDB metadata."""
    result = queries.get_series(
        page=page,
        page_size=page_size,
        search=search,
        genre=genre,
        sort_by=sort_by,
        sort_order=sort_order,
        library_id=library_id,
    )
    return SeriesPaginatedResponse(**result)


@router.get("/series/{series_id}", response_model=SeriesDetailResponse)
def get_series(
    series_id: int,
    language: str | None = Query(None, description="Language parameter ('ar' or 'en')"),
    queries: SeriesQueries = Depends(_get_queries),
) -> SeriesDetailResponse:
    """Return full details for a single TV series."""
    series = queries.get_series_detail(series_id, language=language)
    if series is None:
        raise HTTPException(status_code=404, detail="Series not found")
    return SeriesDetailResponse(**series)


@router.get("/series-genres", response_model=SeriesGenreListResponse)
def list_series_genres(
    library_id: int | None = Query(None, description="Filter by TV library ID"),
    queries: SeriesQueries = Depends(_get_queries),
) -> SeriesGenreListResponse:
    """Return a sorted list of every unique genre across TV series."""
    return SeriesGenreListResponse(genres=queries.get_genres(library_id=library_id))


@router.get("/series-stats", response_model=SeriesStatsResponse)
def series_stats(
    library_id: int | None = Query(None, description="Filter by TV library ID"),
    queries: SeriesQueries = Depends(_get_queries),
) -> SeriesStatsResponse:
    """Return aggregate stats for TV series."""
    return SeriesStatsResponse(**queries.get_stats(library_id=library_id))
