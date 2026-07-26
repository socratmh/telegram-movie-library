from __future__ import annotations

import os
import json
from contextlib import contextmanager
from typing import Iterator, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.models import init_db
from database.tv_models import TVLibrary, TVSeries, TMDBTVSeries


class SeriesDatabase:
    """SQLAlchemy repository for storing scraped TV series records."""

    def __init__(self, database_url: str, library_id: int | None = None) -> None:
        self.SessionLocal = init_db(database_url)
        if library_id is not None:
            self.library_id = library_id
        else:
            env_id = os.environ.get("LIBRARY_ID")
            self.library_id = int(env_id) if env_id else None

    @contextmanager
    def _connection(self) -> Iterator[Session]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_known_titles(self) -> set[str]:
        """Return set of series titles stored for current library."""
        with self._connection() as session:
            query = select(TVSeries.title)
            if self.library_id is not None:
                query = query.where(TVSeries.library_id == self.library_id)
            rows = session.execute(query).scalars().all()
            return set(rows)

    def get_or_create_series(self, title: str, telegram_link: str | None = None) -> int:
        """Find or create a TV series by title. Returns the series ID."""
        with self._connection() as session:
            return self._get_or_create_series(session, title, telegram_link)

    def save_series(self, records: Iterable[dict[str, object]]) -> int:
        """Bulk-save series records. Returns count of newly created entries."""
        saved_count = 0
        with self._connection() as session:
            for record in records:
                title = str(record["title"])
                telegram_link = record.get("telegram_link")
                link = str(telegram_link) if telegram_link else None

                query = select(TVSeries).where(TVSeries.title == title)
                if self.library_id is not None:
                    query = query.where(TVSeries.library_id == self.library_id)

                existing = session.execute(query).scalar_one_or_none()

                if existing is None:
                    series = TVSeries(
                        title=title,
                        telegram_channel_link=link,
                        library_id=self.library_id
                    )
                    session.add(series)
                    try:
                        session.flush()
                        saved_count += 1
                    except IntegrityError:
                        session.rollback()
                elif existing.telegram_channel_link is None and link:
                    existing.telegram_channel_link = link

        return saved_count

    def get_series_without_tmdb(self) -> list[dict[str, object]]:
        """Return series in current library that don't have TMDB data."""
        with self._connection() as session:
            query = select(TVSeries.id, TVSeries.title).where(TVSeries.tmdb_tv_id.is_(None))
            if self.library_id is not None:
                query = query.where(TVSeries.library_id == self.library_id)
            rows = session.execute(query.order_by(TVSeries.title)).all()
            return [{"id": row.id, "title": row.title} for row in rows]

    def save_tmdb_tv(self, tmdb_data: dict[str, object]) -> int:
        """Save TMDB TV metadata. Returns the tmdb_tv_series row ID."""
        with self._connection() as session:
            return self._save_tmdb_tv(session, tmdb_data)

    def link_series_to_tmdb(self, series_id: int, tmdb_tv_id: int) -> None:
        """Link a TV series to its TMDB entry."""
        with self._connection() as session:
            series = session.execute(
                select(TVSeries).where(TVSeries.id == series_id)
            ).scalar_one_or_none()
            if series:
                series.tmdb_tv_id = tmdb_tv_id

    def _get_or_create_series(
        self, session: Session, title: str, telegram_link: str | None
    ) -> int:
        query = select(TVSeries).where(TVSeries.title == title)
        if self.library_id is not None:
            query = query.where(TVSeries.library_id == self.library_id)
        series = session.execute(query).scalars().first()

        if series is None:
            series = TVSeries(
                title=title,
                telegram_channel_link=telegram_link,
                library_id=self.library_id
            )
            session.add(series)
            try:
                session.flush()
            except IntegrityError:
                session.rollback()
                series = session.execute(query).scalars().first()
        elif series.telegram_channel_link is None and telegram_link:
            series.telegram_channel_link = telegram_link

        return int(str(series.id))

    def _save_tmdb_tv(
        self, session: Session, tmdb_data: dict[str, object]
    ) -> int:
        tmdb_id = int(str(tmdb_data["tmdb_id"]))
        existing = session.execute(
            select(TMDBTVSeries).where(TMDBTVSeries.tmdb_id == tmdb_id)
        ).scalar_one_or_none()

        if existing is None:
            genres = tmdb_data.get("genres")
            genres_value = json.dumps(genres if isinstance(genres, list) else [])

            entry = TMDBTVSeries(
                tmdb_id=tmdb_id,
                name=tmdb_data.get("name"),
                original_name=tmdb_data.get("original_name"),
                overview=tmdb_data.get("overview"),
                poster_path=tmdb_data.get("poster_path"),
                backdrop_path=tmdb_data.get("backdrop_path"),
                first_air_date=tmdb_data.get("first_air_date"),
                vote_average=tmdb_data.get("vote_average"),
                number_of_seasons=tmdb_data.get("number_of_seasons"),
                number_of_episodes=tmdb_data.get("number_of_episodes"),
                genres=genres_value,
                status=tmdb_data.get("status"),
            )
            session.add(entry)
            try:
                session.flush()
            except IntegrityError:
                session.rollback()
                entry = session.execute(
                    select(TMDBTVSeries).where(TMDBTVSeries.tmdb_id == tmdb_id)
                ).scalar_one()
            existing = entry

        return int(str(existing.id))
