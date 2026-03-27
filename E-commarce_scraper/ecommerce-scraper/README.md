# E-commerce-Product-Tracker

A production-grade, multi-category ecommerce web scraper that extracts product details, cleans them with pandas, and exports both CSV and Excel.

## Features
- Scrapes multiple product categories (laptops, tablets, phones/touch)
- Robust HTML parsing with graceful handling of missing fields
- Connection pooling via `requests.Session()`
- Polite crawling with a configurable request delay
- Data cleaning & transformation using `pandas`
- Exports results to both `.csv` and `.xlsx`
- Detailed logging of pages scraped and errors

## Tech Stack
- Python 3
- Requests for HTTP
- BeautifulSoup4 for HTML parsing
- Pandas for data cleaning/export
- OpenPyXL for Excel output

Badges:

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)
![requests](https://img.shields.io/badge/requests-25A162?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-1.12.0-4B8BBE?style=for-the-badge)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)
![openpyxl](https://img.shields.io/badge/openpyxl-3.x-1E90FF?style=for-the-badge)

## Project Structure
```text
ecommerce-scraper/
├── scraper/
│   ├── __init__.py
│   ├── core.py          # main scraping logic
│   └── utils.py         # helper functions (headers, delays, etc.)
├── cleaner/
│   ├── __init__.py
│   └── transform.py     # pandas data cleaning & transformation
├── output/              # auto-created at runtime
├── logs/                # auto-created at runtime
├── main.py              # entry point
├── config.py            # all config (URLs, settings) in one place
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codewithmahfuz/product-price-tracker.git
   cd ecommerce-scraper
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the scraper:
```bash
python main.py
```

The script will:
1. Scrape all configured categories
2. Clean/transform the raw data with pandas
3. Save outputs into `output/`

## Output
Generated files (under `output/`):
- `ecommerce_products.csv`
- `ecommerce_products.xlsx`

Example preview (columns):
```text
Category       | Title                 | Price (USD) | Rating | Description
--------------- | --------------------- | ------------ | ------- | -----------------------------------------
Laptops         | Asus VivoBook X441...| 295.99       | 3.0     | Asus VivoBook X441NA-GA190 ...
Tablets         | Lenovo ThinkPad ...  | 408.56       | 4.0     | ...
Phones/touch    | Sony Xperia ...      | 468.56       | 5.0     | ...
```

## Configuration
All URLs and settings live in `config.py`.

Key settings:
- `BASE_URLS`: category keys mapped to their base listing URLs
- `REQUEST_DELAY`: seconds between HTTP requests
- `USER_AGENT`: browser-like user agent string
- `OUTPUT_DIR` / `LOG_DIR`: output and logging directories

To change categories or targets, edit `BASE_URLS` and re-run:
```python
BASE_URLS = {
    "laptops": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
    "tablets": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
    "phones/touch": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
}
```

## Author
- Replace this section with your details:
  - Name: Mahfuzur Rahman Chowdhury
  - Email: codingwithmahfuz@gmail.com
  - GitHub: https://codingwithmahfuz/github.com/<codingwithmahfuz>

