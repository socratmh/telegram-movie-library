from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Text

from database.models import Base


class SiteVisit(Base):
    """Tracks individual page visits for analytics."""
    __tablename__ = 'site_visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    visitor_id = Column(String, nullable=False, index=True)  # UUID from localStorage
    ip_address = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    device_type = Column(String, nullable=True)   # Desktop / Mobile / Tablet
    os = Column(String, nullable=True)            # Windows / Android / iOS / Linux / macOS
    browser = Column(String, nullable=True)       # Chrome / Firefox / Edge / Safari
    referrer = Column(String, nullable=True)      # Direct / Google / Telegram / Facebook
    page_path = Column(String, nullable=True)     # e.g. "/" or "/library/movies"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
