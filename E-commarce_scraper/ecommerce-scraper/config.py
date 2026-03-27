"""
Central configuration for the ecommerce scraper.
"""

from __future__ import annotations

from typing import Final


# Base directory names (directories are created at runtime if missing).
OUTPUT_DIR: Final[str] = "output"
LOG_DIR: Final[str] = "logs"

# Delay between HTTP requests to be polite to the target site.
REQUEST_DELAY: Final[float] = 1.0

# Realistic browser user agent.
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT: Final[int] = 30

# HTTP header configuration.
HTTP_ACCEPT: Final[str] = "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8"
HTTP_ACCEPT_LANGUAGE: Final[str] = "en-US,en;q=0.9"
HTTP_CONNECTION: Final[str] = "keep-alive"

# Category listing configuration for the target site.
# NOTE: These are the category pages that render the product cards server-side.
BASE_URLS: Final[dict[str, str]] = {
    "laptops": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
    "tablets": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
    "phones/touch": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
}

# Pagination settings. For this particular test site, pages are typically pre-rendered,
# but these settings allow safe extension if pagination links are ever present.
PAGE_PARAM: Final[str] = "page"
PAGE_START: Final[int] = 1
MAX_PAGES: Final[int] = 20

# Scraper CSS selectors / extraction hints.
PRODUCT_CARD_SELECTOR: Final[str] = "div.product-wrapper"
TITLE_SELECTOR: Final[str] = "a.title"
PRICE_SELECTOR: Final[str] = "h4.price"
RATING_SELECTOR: Final[str] = "p[data-rating]"
DESCRIPTION_SELECTOR: Final[str] = "p.description"

# Individual extraction hints (used by BeautifulSoup ``find`` calls).
TITLE_CLASS: Final[str] = "title"
PRICE_CLASS: Final[str] = "price"
RATING_ATTRIBUTE: Final[str] = "data-rating"
DESCRIPTION_CLASS: Final[str] = "description"

# Output filenames (saved into OUTPUT_DIR at runtime).
CSV_FILENAME: Final[str] = "ecommerce_products.csv"
EXCEL_FILENAME: Final[str] = "ecommerce_products.xlsx"

