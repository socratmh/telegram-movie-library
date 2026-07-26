from __future__ import annotations

from dataclasses import dataclass
import re


TELEGRAM_LINK_PATTERN = re.compile(
    r"https?://t\.me/[^\s\"'<>]+",
    re.IGNORECASE,
)

NOISE_PATTERNS = (
    re.compile(r"\b(?:download|watch|series|season|episode|new link)\b", re.IGNORECASE),
    re.compile(r"https?://\S+", re.IGNORECASE),
    re.compile(r"@\w+"),
    re.compile(r"#[\w-]+"),
)


@dataclass(frozen=True)
class ParsedSeries:
    title: str
    telegram_link: str | None


def parse_series_message(message_text: str | None) -> ParsedSeries | None:
    """
    Extract a TV series title and Telegram channel link from a message.

    Expected message format:
    - Title on the first meaningful line
    - A t.me link somewhere in the message body
    """
    if not message_text:
        return None

    # Extract all Telegram links from the full message
    links = TELEGRAM_LINK_PATTERN.findall(message_text)
    telegram_link = links[0] if links else None

    # Find the title from the first non-empty line
    candidates = [
        line.strip()
        for line in message_text.splitlines()
        if line.strip()
    ]

    for candidate in candidates:
        title = _clean_title(candidate)
        if _is_valid_title(title):
            return ParsedSeries(title=title, telegram_link=telegram_link)

    return None


def _clean_title(text: str) -> str:
    text = text.replace("_", " ")

    # Remove Arabic characters
    text = re.sub(r"[\u0600-\u06FF]+", " ", text)

    # Remove emojis and non-standard symbols (keep words, spaces, and basic punctuation)
    text = re.sub(r"[^\w\s\.,!\?:\-\'\"()\[\]&]", " ", text)

    text = re.sub(r"[\[\]{}]", " ", text)

    for pattern in NOISE_PATTERNS:
        text = pattern.sub(" ", text)

    text = re.sub(r"[-|:]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,-:;|")


def _is_valid_title(title: str) -> bool:
    if len(title) < 2:
        return False

    if len(title.split()) > 15:
        return False

    if not re.search(r"[A-Za-z0-9]", title):
        return False

    # Skip lines that look like just a URL
    if title.startswith("http"):
        return False

    return True
