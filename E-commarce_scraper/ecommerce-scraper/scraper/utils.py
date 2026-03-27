"""
Utility helpers for the ecommerce scraper.

The functions in this module are designed to be small, testable, and robust.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup, Tag

from config import (
    HTTP_ACCEPT,
    HTTP_ACCEPT_LANGUAGE,
    HTTP_CONNECTION,
    REQUEST_DELAY,
    USER_AGENT,
)


def build_session_headers(user_agent: str) -> dict[str, str]:
    """
    Build request headers used by :class:`requests.Session`.

    Args:
        user_agent: Browser user agent string.

    Returns:
        A dictionary of HTTP headers.
    """

    return {
        "User-Agent": user_agent,
        "Accept": HTTP_ACCEPT,
        "Accept-Language": HTTP_ACCEPT_LANGUAGE,
        "Connection": HTTP_CONNECTION,
    }


def sleep_between_requests(delay: float = REQUEST_DELAY) -> None:
    """
    Sleep for the configured delay between requests.

    Args:
        delay: Number of seconds to sleep.
    """

    time.sleep(delay)


def get_logger(logger: Optional[logging.Logger] = None) -> logging.Logger:
    """
    Get a usable logger instance.

    Args:
        logger: Optional logger provided by the caller.

    Returns:
        A logger that can be used for logging.
    """

    return logger if logger is not None else logging.getLogger("ecommerce_scraper")


def safe_find(tag: Optional[Tag], name: str, **kwargs: Any) -> Optional[Tag]:
    """
    Safely call ``tag.find(...)`` and return the result.

    This helper ensures we don't crash on missing/invalid elements.

    Args:
        tag: Parent BeautifulSoup tag.
        name: Tag name to find.
        **kwargs: Additional keyword arguments passed to ``find``.

    Returns:
        The found :class:`bs4.Tag` or ``None`` if missing.
    """

    if tag is None:
        return None

    try:
        return tag.find(name, **kwargs)
    except (AttributeError, TypeError):
        return None


def safe_find_attr(tag: Optional[Tag], attr_name: str) -> Optional[str]:
    """
    Safely read an attribute from a BeautifulSoup tag.

    Args:
        tag: Tag to read from.
        attr_name: Attribute key.

    Returns:
        Attribute value as a string, or ``None`` if missing.
    """

    if tag is None:
        return None

    try:
        value = tag.get(attr_name)
        return str(value) if value is not None else None
    except (AttributeError, TypeError):
        return None


def safe_get_text(tag: Optional[Tag], *, strip: bool = True, sep: str = " ") -> Optional[str]:
    """
    Safely extract text from a BeautifulSoup tag.

    Args:
        tag: Tag to extract from.
        strip: Whether to strip whitespace.
        sep: Separator passed to BeautifulSoup's ``get_text``.

    Returns:
        Extracted text or ``None``.
    """

    if tag is None:
        return None

    try:
        return tag.get_text(separator=sep, strip=strip)
    except (AttributeError, TypeError):
        return None


def make_session(user_agent: str = USER_AGENT) -> requests.Session:
    """
    Create a configured :class:`requests.Session` instance.

    Args:
        user_agent: Browser user agent string.

    Returns:
        Configured session.
    """

    session = requests.Session()
    session.headers.update(build_session_headers(user_agent))
    return session


def parse_html(html: str) -> BeautifulSoup:
    """
    Parse HTML into a BeautifulSoup object.

    Args:
        html: Raw HTML.

    Returns:
        BeautifulSoup instance.
    """

    return BeautifulSoup(html, "html.parser")

