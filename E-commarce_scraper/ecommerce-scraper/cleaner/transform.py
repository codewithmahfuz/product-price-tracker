"""
Pandas-based cleaning and transformation utilities.

This module converts the raw product dictionaries returned by the scraper into
cleaned, typed pandas DataFrames suitable for analytics and export.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from config import (
    CSV_FILENAME,
    EXCEL_FILENAME,
    OUTPUT_DIR,
)

logger = logging.getLogger("ecommerce_scraper")


def _strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip whitespace from all string columns (object dtype).

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with stripped whitespace in string columns.
    """

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def _parse_price_to_float(value: Any) -> Optional[float]:
    """
    Convert a raw price string like ``$295.99`` into a float.

    Args:
        value: Raw value from the scraper.

    Returns:
        Parsed float or ``None`` if conversion is not possible.
    """

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    raw = str(value)
    raw = raw.replace("$", "").replace(",", "").strip()
    raw = raw.replace("+", "")

    match = re.search(r"([0-9]+(?:\\.[0-9]+)?)", raw)
    if not match:
        return None
    try:
        return float(match.group(1))
    except (TypeError, ValueError):
        return None


def clean_data(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Clean and transform raw scraped data into a normalized DataFrame.

    Cleaning steps:
    - Strip ``$`` from price and convert to ``float``.
    - Convert rating to ``float`` (missing -> NaN).
    - Strip whitespace from all string columns.
    - Remove exact duplicate rows.
    - Rename columns to the desired output schema.

    Args:
        raw_data: List of raw product dictionaries.

    Returns:
        Cleaned pandas DataFrame.
    """

    if not raw_data:
        df = pd.DataFrame(columns=["Category", "Title", "Price (USD)", "Rating", "Description"])
        return df

    df = pd.DataFrame(raw_data)

    # Ensure expected columns exist (missing fields become None).
    for col in ["category", "title", "price", "rating", "description"]:
        if col not in df.columns:
            df[col] = None

    # Price
    df["price"] = df["price"].apply(_parse_price_to_float).astype("float64")

    # Rating
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("float64")

    # Strip whitespace from string columns
    df = _strip_string_columns(df)

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Rename columns
    df = df.rename(
        columns={
            "category": "Category",
            "title": "Title",
            "price": "Price (USD)",
            "rating": "Rating",
            "description": "Description",
        }
    )

    # Re-order columns for a stable output schema.
    df = df[["Category", "Title", "Price (USD)", "Rating", "Description"]]

    # Summary (as requested). This is client-facing output.
    if not df.empty:
        summary = (
            df.groupby("Category", dropna=False)
            .agg(
                Total_Products=("Title", "count"),
                Avg_Price=("Price (USD)", "mean"),
                Avg_Rating=("Rating", "mean"),
            )
            .reset_index()
        )
        summary["Avg_Price"] = summary["Avg_Price"].round(2)
        summary["Avg_Rating"] = summary["Avg_Rating"].round(2)
        print("\nScraping Summary by Category")
        print(summary.to_string(index=False))
    else:
        print("\nScraping Summary by Category")
        print("No products were scraped.")

    return df


def save_outputs(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Save cleaned DataFrame to both CSV and Excel formats.

    Output files are written into ``output/`` (configured by :data:`config.OUTPUT_DIR`).

    Args:
        df: Cleaned pandas DataFrame.

    Returns:
        Tuple of ``(csv_path, xlsx_path)``.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    csv_path = os.path.join(OUTPUT_DIR, CSV_FILENAME)
    xlsx_path = os.path.join(OUTPUT_DIR, EXCEL_FILENAME)

    df.to_csv(csv_path, index=False, encoding="utf-8")
    logger.info("Saved CSV: %s", csv_path)

    # Excel requires openpyxl for xlsx writing.
    df.to_excel(xlsx_path, index=False)
    logger.info("Saved Excel: %s", xlsx_path)

    return csv_path, xlsx_path

