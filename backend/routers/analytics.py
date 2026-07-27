"""Analytics router — visitor tracking (public) + admin analytics endpoints."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any

import requests as http_requests
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select, func, distinct, desc, cast, String as SAString
from user_agents import parse as parse_ua

from backend.auth import get_current_admin
from database.analytics_models import SiteVisit
from database.models import init_db

router = APIRouter(tags=["analytics"])


# ------------------------------------------------------------------
# Pydantic models
# ------------------------------------------------------------------

class TrackRequest(BaseModel):
    visitor_id: str
    page: str = "/"
    referrer: str = ""
    screen_width: int | None = None


class AnalyticsSummary(BaseModel):
    total_visits: int
    unique_visitors: int
    active_today: int
    active_this_week: int
    active_this_month: int


class VisitorRecord(BaseModel):
    id: int
    visitor_id: str
    ip_address: str | None
    country: str | None
    city: str | None
    device_type: str | None
    os: str | None
    browser: str | None
    referrer: str | None
    page_path: str | None
    created_at: str | None


class VisitorListResponse(BaseModel):
    items: list[VisitorRecord]
    total: int
    page: int
    page_size: int
    total_pages: int


class BreakdownItem(BaseModel):
    label: str
    count: int


class BreakdownResponse(BaseModel):
    by_country: list[BreakdownItem]
    by_device: list[BreakdownItem]
    by_os: list[BreakdownItem]
    by_browser: list[BreakdownItem]
    top_pages: list[BreakdownItem]
    by_referrer: list[BreakdownItem]


class ChartPoint(BaseModel):
    label: str
    count: int


class ChartsResponse(BaseModel):
    daily: list[ChartPoint]
    monthly: list[ChartPoint]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

_GEO_CACHE: dict[str, dict[str, str]] = {}


def _get_session_factory(request: Request):
    return request.app.state.queries.SessionLocal


def _classify_referrer(raw: str) -> str:
    if not raw or raw.strip() == "":
        return "Direct"
    r = raw.lower()
    if "google" in r:
        return "Google"
    if "t.me" in r or "telegram" in r:
        return "Telegram"
    if "facebook" in r or "fb.com" in r:
        return "Facebook"
    if "twitter" in r or "x.com" in r:
        return "Twitter/X"
    if "instagram" in r:
        return "Instagram"
    if "youtube" in r:
        return "YouTube"
    if "reddit" in r:
        return "Reddit"
    if "tiktok" in r:
        return "TikTok"
    return raw[:60]


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "unknown"


def _lookup_geo(ip: str) -> dict[str, str]:
    if ip in _GEO_CACHE:
        return _GEO_CACHE[ip]
    if ip in ("127.0.0.1", "::1", "localhost", "unknown"):
        result = {"country": "Local", "city": "Local"}
        _GEO_CACHE[ip] = result
        return result
    try:
        resp = http_requests.get(f"http://ip-api.com/json/{ip}?fields=country,city", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            result = {
                "country": data.get("country", "Unknown"),
                "city": data.get("city", ""),
            }
            _GEO_CACHE[ip] = result
            return result
    except Exception:
        pass
    result = {"country": "Unknown", "city": ""}
    _GEO_CACHE[ip] = result
    return result


def _parse_device(ua_string: str, screen_width: int | None) -> dict[str, str]:
    ua = parse_ua(ua_string)
    # Device type
    if ua.is_mobile:
        device = "Mobile"
    elif ua.is_tablet:
        device = "Tablet"
    elif ua.is_pc:
        device = "Desktop"
    elif screen_width and screen_width < 768:
        device = "Mobile"
    else:
        device = "Desktop"

    # OS
    os_family = ua.os.family or "Unknown"

    # Browser
    browser_family = ua.browser.family or "Unknown"

    return {"device_type": device, "os": os_family, "browser": browser_family}


# ------------------------------------------------------------------
# Public tracking endpoint
# ------------------------------------------------------------------

@router.post("/api/track", status_code=200)
def track_visit(body: TrackRequest, request: Request):
    """Record a page visit. Public, no auth."""
    ip = _get_client_ip(request)
    geo = _lookup_geo(ip)
    ua_string = request.headers.get("user-agent", "")
    device_info = _parse_device(ua_string, body.screen_width)
    referrer = _classify_referrer(body.referrer)

    SessionLocal = _get_session_factory(request)
    with SessionLocal() as session:
        visit = SiteVisit(
            visitor_id=body.visitor_id,
            ip_address=ip,
            country=geo["country"],
            city=geo["city"],
            device_type=device_info["device_type"],
            os=device_info["os"],
            browser=device_info["browser"],
            referrer=referrer,
            page_path=body.page,
        )
        session.add(visit)
        session.commit()

    return {"status": "ok"}


# ------------------------------------------------------------------
# Admin analytics endpoints
# ------------------------------------------------------------------

@router.get("/api/admin/analytics/summary", response_model=AnalyticsSummary,
            dependencies=[Depends(get_current_admin)])
def analytics_summary(request: Request):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    SessionLocal = _get_session_factory(request)
    with SessionLocal() as session:
        total_visits = session.scalar(select(func.count(SiteVisit.id))) or 0
        unique_visitors = session.scalar(
            select(func.count(distinct(SiteVisit.visitor_id)))
        ) or 0
        active_today = session.scalar(
            select(func.count(distinct(SiteVisit.visitor_id)))
            .where(SiteVisit.created_at >= today_start)
        ) or 0
        active_week = session.scalar(
            select(func.count(distinct(SiteVisit.visitor_id)))
            .where(SiteVisit.created_at >= week_start)
        ) or 0
        active_month = session.scalar(
            select(func.count(distinct(SiteVisit.visitor_id)))
            .where(SiteVisit.created_at >= month_start)
        ) or 0

    return AnalyticsSummary(
        total_visits=total_visits,
        unique_visitors=unique_visitors,
        active_today=active_today,
        active_this_week=active_week,
        active_this_month=active_month,
    )


@router.get("/api/admin/analytics/visitors", response_model=VisitorListResponse,
            dependencies=[Depends(get_current_admin)])
def analytics_visitors(
    request: Request,
    page: int = 1,
    page_size: int = 50,
):
    SessionLocal = _get_session_factory(request)
    with SessionLocal() as session:
        total = session.scalar(select(func.count(SiteVisit.id))) or 0
        offset = (page - 1) * page_size
        rows = session.execute(
            select(SiteVisit)
            .order_by(desc(SiteVisit.created_at))
            .limit(page_size)
            .offset(offset)
        ).scalars().all()

        items = [
            VisitorRecord(
                id=v.id,
                visitor_id=v.visitor_id[:12] + "…",
                ip_address=v.ip_address,
                country=v.country,
                city=v.city,
                device_type=v.device_type,
                os=v.os,
                browser=v.browser,
                referrer=v.referrer,
                page_path=v.page_path,
                created_at=v.created_at.isoformat() if v.created_at else None,
            )
            for v in rows
        ]

    import math
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    return VisitorListResponse(
        items=items, total=total, page=page,
        page_size=page_size, total_pages=total_pages,
    )


@router.get("/api/admin/analytics/breakdown", response_model=BreakdownResponse,
            dependencies=[Depends(get_current_admin)])
def analytics_breakdown(request: Request):
    SessionLocal = _get_session_factory(request)
    with SessionLocal() as session:
        def _top(col, limit=10):
            rows = session.execute(
                select(col, func.count(SiteVisit.id).label("cnt"))
                .where(col.isnot(None))
                .where(col != "")
                .group_by(col)
                .order_by(desc("cnt"))
                .limit(limit)
            ).all()
            return [BreakdownItem(label=r[0] or "Unknown", count=r[1]) for r in rows]

        return BreakdownResponse(
            by_country=_top(SiteVisit.country),
            by_device=_top(SiteVisit.device_type),
            by_os=_top(SiteVisit.os),
            by_browser=_top(SiteVisit.browser),
            top_pages=_top(SiteVisit.page_path, 15),
            by_referrer=_top(SiteVisit.referrer),
        )


@router.get("/api/admin/analytics/charts", response_model=ChartsResponse,
            dependencies=[Depends(get_current_admin)])
def analytics_charts(request: Request):
    SessionLocal = _get_session_factory(request)
    now = datetime.now(timezone.utc)

    with SessionLocal() as session:
        # Daily visits — last 30 days
        thirty_days_ago = now - timedelta(days=30)
        daily_rows = session.execute(
            select(
                func.date(SiteVisit.created_at).label("day"),
                func.count(SiteVisit.id).label("cnt"),
            )
            .where(SiteVisit.created_at >= thirty_days_ago)
            .group_by("day")
            .order_by("day")
        ).all()
        daily = [ChartPoint(label=str(r[0]), count=r[1]) for r in daily_rows]

        # Monthly visits — last 12 months
        twelve_months_ago = now - timedelta(days=365)
        # Use substr for cross-DB compatibility (SQLite + PostgreSQL)
        month_expr = func.substr(cast(SiteVisit.created_at, SAString), 1, 7)
        monthly_rows = session.execute(
            select(
                month_expr.label("month"),
                func.count(SiteVisit.id).label("cnt"),
            )
            .where(SiteVisit.created_at >= twelve_months_ago)
            .group_by("month")
            .order_by("month")
        ).all()
        monthly = [ChartPoint(label=str(r[0]), count=r[1]) for r in monthly_rows]

    return ChartsResponse(daily=daily, monthly=monthly)
