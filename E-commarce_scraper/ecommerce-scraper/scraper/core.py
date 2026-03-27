"""
Core scraping logic for the ecommerce scraper.

This module contains the :class:`EcommerceScraper` class which is responsible
for retrieving product listings from configured categories and returning raw
product dictionaries for downstream cleaning.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

import requests
from bs4 import BeautifulSoup, Tag

from config import (
    BASE_URLS,
    DESCRIPTION_SELECTOR,
    MAX_PAGES,
    PAGE_PARAM,
    PAGE_START,
    PRICE_SELECTOR,
    PRODUCT_CARD_SELECTOR,
    RATING_SELECTOR,
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    TITLE_SELECTOR,
    DESCRIPTION_CLASS,
    PRICE_CLASS,
    RATING_ATTRIBUTE,
    TITLE_CLASS,
)
from scraper.utils import make_session, parse_html, safe_find, safe_find_attr, safe_get_text


@dataclass(frozen=True)
class ProductRaw:
    """
    A lightweight container for raw product fields.

    The cleaner is responsible for normalization and type conversions.
    """

    category: str
    title: Optional[str]
    price: Optional[str]
    rating: Optional[str]
    description: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this instance to a dictionary matching the raw schema.

        Returns:
            Dictionary with keys: category, title, price, rating, description.
        """

        return {
            "category": self.category,
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "description": self.description,
        }


class EcommerceScraper:
    """
    Scrape product data from the Web Scraper Test Sites (Allinone).

    The scraper returns raw dictionaries which are later cleaned using pandas.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the scraper with a configured HTTP session and logger.

        Args:
            logger: Optional logger. If omitted, a default logger is used.
        """

        self.logger = logger or logging.getLogger("ecommerce_scraper")
        self.session = make_session()

    def _build_page_url(self, base_url: str, page_num: int) -> str:
        """
        Build a category page URL for the given page number.

        Args:
            base_url: Base category URL.
            page_num: Page index (1-based).

        Returns:
            Fully qualified URL.
        """

        if page_num == PAGE_START:
            return base_url
        return f"{base_url}?{PAGE_PARAM}={page_num}"

    def _extract_product_from_card(self, category_name: str, card: Tag) -> ProductRaw:
        """
        Extract raw fields from a single product card.

        Missing fields are returned as ``None``.

        Args:
            category_name: Human readable category key.
            card: BeautifulSoup Tag representing the product card.

        Returns:
            A :class:`ProductRaw` instance.
        """

        # Title
        title_link = safe_find(card, "a", class_=TITLE_CLASS)
        title = safe_get_text(title_link)

        # Price
        price_el = safe_find(card, "h4", class_=PRICE_CLASS)
        price_text = safe_get_text(price_el)

        # Rating
        rating_el = safe_find(card, "p", attrs={RATING_ATTRIBUTE: True})
        rating = safe_find_attr(rating_el, RATING_ATTRIBUTE)

        # Description
        desc_el = safe_find(card, "p", class_=DESCRIPTION_CLASS)
        description = safe_get_text(desc_el)

        return ProductRaw(
            category=category_name,
            title=title,
            price=price_text,
            rating=rating,
            description=description,
        )

    def scrape_category(self, category_name: str, base_url: str) -> List[Dict[str, Any]]:
        """
        Scrape all pages of one category.

        Args:
            category_name: Key used for the output category field.
            base_url: Category listing URL.

        Returns:
            List of raw product dictionaries.
        """

        products: List[Dict[str, Any]] = []
        seen_product_identifiers: Set[str] = set()

        for page_num in range(PAGE_START, MAX_PAGES + 1):
            page_url = self._build_page_url(base_url, page_num)
            self.logger.info("Scraping category=%s page=%s url=%s", category_name, page_num, page_url)

            try:
                response = self.session.get(page_url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
            except requests.exceptions.Timeout as exc:
                self.logger.error(
                    "Timeout while scraping category=%s page=%s: %s",
                    category_name,
                    page_num,
                    exc,
                    exc_info=True,
                )
                continue
            except requests.exceptions.ConnectionError as exc:
                self.logger.error(
                    "Connection error while scraping category=%s page=%s: %s",
                    category_name,
                    page_num,
                    exc,
                    exc_info=True,
                )
                continue
            except requests.exceptions.RequestException as exc:
                self.logger.error(
                    "Request error while scraping category=%s page=%s: %s",
                    category_name,
                    page_num,
                    exc,
                    exc_info=True,
                )
                continue

            soup = parse_html(response.text)
            try:
                cards = soup.select(PRODUCT_CARD_SELECTOR)
            except Exception as exc:  # noqa: BLE001 - defensive against selector issues
                self.logger.error(
                    "HTML parsing error category=%s page=%s: %s",
                    category_name,
                    page_num,
                    exc,
                    exc_info=True,
                )
                continue

            page_count = 0
            new_identifiers: Set[str] = set()
            for card in cards:
                product = self._extract_product_from_card(category_name, card)
                identifier = product.title or product.price or str(len(products))
                new_identifiers.add(identifier)
                if identifier in seen_product_identifiers:
                    continue
                seen_product_identifiers.add(identifier)
                products.append(product.to_dict())
                page_count += 1

            self.logger.info(
                "Scraped category=%s page=%s new_products=%s total_products=%s",
                category_name,
                page_num,
                page_count,
                len(products),
            )

            if page_count == 0:
                # If pagination doesn't change content, stop early.
                self.logger.info("No new products found; stopping category=%s", category_name)
                break

            time.sleep(REQUEST_DELAY)

        return products

    def scrape_all(self) -> List[Dict[str, Any]]:
        """
        Scrape all configured categories and return raw product dictionaries.

        Returns:
            Combined list of raw product dictionaries from all categories.
        """

        all_products: List[Dict[str, Any]] = []

        for category_name, base_url in BASE_URLS.items():
            self.logger.info("Starting scrape for category=%s base_url=%s", category_name, base_url)
            category_products = self.scrape_category(category_name=category_name, base_url=base_url)
            all_products.extend(category_products)

        return all_products

