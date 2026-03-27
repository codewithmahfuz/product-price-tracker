# Ecommerce Product Tracker

A production-grade, multi-category ecommerce web scraper built with Python. Extracts product details across multiple categories, cleans the data with pandas, and exports to both CSV and Excel.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## Overview

This tool automates the full data collection pipeline for ecommerce products:

1. **Scrapes** product listings from multiple categories (laptops, tablets, phones)
2. **Cleans** raw data using pandas — handles missing fields, normalizes prices, strips whitespace
3. **Exports** a clean dataset to `.csv` and `.xlsx` with one command

Targets [webscraper.io's test ecommerce site](https://webscraper.io/test-sites/e-commerce/allinone) — safe for practice and portfolio use.

---

## Features

- Multi-category scraping in a single run
- Connection pooling via `requests.Session()` for efficiency
- Graceful handling of missing or malformed fields
- Configurable request delay for polite crawling
- Structured logging per run (saved to `logs/`)
- Dual export: `.csv` and `.xlsx`

---

## Project Structure

```
ecommerce-scraper/
├── scraper/
│   ├── __init__.py
│   ├── core.py          # Scraping logic
│   └── utils.py         # Headers, delays, helpers
├── cleaner/
│   ├── __init__.py
│   └── transform.py     # Pandas cleaning & transformation
├── output/              # Generated at runtime
├── logs/                # Generated at runtime
├── main.py              # Entry point
├── config.py            # URLs and settings
└── requirements.txt
```

---

## Installation

**Requirements:** Python 3.8+

```bash
# 1. Clone the repo
git clone https://github.com/codewithmahfuz/product-price-tracker.git
cd ecommerce-scraper

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

Output files are saved to `output/`:

```
output/
├── ecommerce_products.csv
└── ecommerce_products.xlsx
```

---

## Configuration

All settings are in `config.py`:

```python
BASE_URLS = {
    "laptops":      "https://webscraper.io/.../computers/laptops",
    "tablets":      "https://webscraper.io/.../computers/tablets",
    "phones/touch": "https://webscraper.io/.../phones/touch",
}

REQUEST_DELAY = 1.5   # seconds between requests
OUTPUT_DIR    = "output/"
LOG_DIR       = "logs/"
```

To scrape different categories, update `BASE_URLS` and re-run.

---

## Sample Output

| Category | Title | Price (USD) | Rating |
|---|---|---|---|
| Laptops | Asus VivoBook X441NA | 295.99 | 3.0 |
| Tablets | Lenovo ThinkPad 10 | 408.56 | 4.0 |
| Phones/Touch | Sony Xperia Z3+ | 468.56 | 5.0 |

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests and session management |
| `beautifulsoup4` | HTML parsing |
| `pandas` | Data cleaning and transformation |
| `openpyxl` | Excel export engine |

Install all at once:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Author

**Mahfuzur Rahman Chowdhury**  
[github.com/codewithmahfuz](https://github.com/codewithmahfuz) · codingwithmahfuz@gmail.com
