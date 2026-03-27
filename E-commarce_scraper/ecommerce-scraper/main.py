"""
Entry point for the ecommerce scraper.

Run this script with:

    python main.py
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

from cleaner.transform import clean_data, save_outputs
from scraper.core import EcommerceScraper

from config import LOG_DIR, OUTPUT_DIR


def setup_logger(log_dir: str = LOG_DIR, log_level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return the application's root logger.

    Args:
        log_dir: Directory where the log file will be written.
        log_level: Logging level for handlers.

    Returns:
        Configured :class:`logging.Logger` instance.
    """

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logger = logging.getLogger("ecommerce_scraper")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        # Avoid duplicate handlers when re-running in interactive sessions.
        return logger

    log_filename = f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = os.path.join(log_dir, log_filename)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.debug("Logger initialized at %s", log_path)
    return logger


def main() -> None:
    """
    Run the full scrape -> clean -> export pipeline.
    """

    logger = setup_logger()

    logger.info("Starting ecommerce scraping pipeline")

    scraper = EcommerceScraper(logger=logger)
    raw_data = scraper.scrape_all()
    logger.info("Scraping complete. Raw products retrieved: %s", len(raw_data))

    df = clean_data(raw_data)
    logger.info("Cleaning complete. Cleaned rows: %s", len(df))

    csv_path, xlsx_path = save_outputs(df)

    logger.info("Outputs saved successfully: %s and %s", csv_path, xlsx_path)
    print("\nSuccess! Outputs generated:")
    print(f"- CSV: {csv_path}")
    print(f"- Excel: {xlsx_path}")


if __name__ == "__main__":
    main()

