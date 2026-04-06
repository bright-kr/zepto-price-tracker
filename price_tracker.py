"""
Zepto Price Tracker - Bright Data Web Scraper API
----------------------------------------------------
Track prices, availability, and product data from Zepto.

Docs  : https://docs.brightdata.co.kr/scraping-automation/web-scraper-api/overview
Info  : https://brightdata.co.kr/products/insights/price-tracker/zepto
"""

import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────
API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN", "")
if not API_TOKEN:
    raise EnvironmentError(
        "BRIGHTDATA_API_TOKEN is not set.\n"
        "1. Get your token at: https://docs.brightdata.co.kr/general/account/account-settings#api-token\n"
        "2. Add it to your .env file: BRIGHTDATA_API_TOKEN=<your_token>"
    )

# Set your Web Scraper ID after building your Zepto scraper:
# https://brightdata.co.kr/products/web-scraper/zepto
DATASET_ID = os.getenv("BRIGHTDATA_DATASET_ID", "")
if not DATASET_ID:
    raise EnvironmentError(
        "BRIGHTDATA_DATASET_ID is not set.\n"
        "1. Build your Zepto scraper at: https://brightdata.co.kr/products/web-scraper/zepto\n"
        "2. Copy the resulting Web Scraper ID (format: gd_xxxxxxxxxx).\n"
        "3. Add it to your .env file: BRIGHTDATA_DATASET_ID=<your_scraper_id>"
    )

_BASE = "https://api.brightdata.co.kr/datasets/v3"
_HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


# ── Core API functions ─────────────────────────────────────────────────────────

def trigger_collection(
    inputs: list[dict],
    limit: int | None = None,
    notify: str | None = None,
    include_errors: bool = True,
) -> str:
    """
    Trigger a dataset collection job.

    Args:
        inputs: List of dicts - each with a "url" key (or keyword/category params).
        limit: Max records to return (None = no limit).
        notify: Optional webhook URL called when the snapshot completes.
        include_errors: Include per-record error details in results.

    Returns:
        snapshot_id string, used to poll for results.
    """
    params: dict = {"dataset_id": DATASET_ID, "include_errors": include_errors}
    if limit is not None:
        params["limit_multiple_results"] = limit
    if notify:
        params["notify"] = notify

    response = requests.post(
        f"{_BASE}/trigger",
        headers=_HEADERS,
        params=params,
        json=inputs,
        timeout=60,
    )
    response.raise_for_status()
    snapshot_id: str = response.json()["snapshot_id"]
    print(f"[✓] Collection triggered - snapshot_id: {snapshot_id}")
    return snapshot_id


def get_results(snapshot_id: str, poll_interval: int = 10) -> list[dict]:
    """
    Poll until the snapshot is ready and return all collected records.

    Args:
        snapshot_id: ID returned by trigger_collection().
        poll_interval: Seconds between status checks (default 10).

    Returns:
        List of product record dicts.
    """
    url = f"{_BASE}/snapshot/{snapshot_id}"
    params = {"format": "json"}

    while True:
        resp = requests.get(url, headers=_HEADERS, params=params, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            # API may return a list directly or {results: [...]}
            records = data if isinstance(data, list) else data.get("results", data)
            print(f"[✓] Snapshot ready - {len(records)} record(s) returned.")
            return records
        elif resp.status_code == 202:
            progress = resp.json().get("status", "processing")
            print(f"[…] Status: {progress} - retrying in {poll_interval}s")
            time.sleep(poll_interval)
        else:
            resp.raise_for_status()


# ── High-level helpers ─────────────────────────────────────────────────────────

def track_prices(urls: list[str], **kwargs) -> list[dict]:
    """
    Collect price data for a list of Zepto product URLs.

    Example:
        results = track_prices([
            "https://www.zeptonow.com/products/sample-product",
        ])
    """
    inputs = [{"url": u} for u in urls]
    snapshot_id = trigger_collection(inputs, **kwargs)
    return get_results(snapshot_id)


def discover_by_keyword(keyword: str, limit: int = 50, **kwargs) -> list[dict]:
    """
    Discover Zepto products by keyword search.

    Example:
        results = discover_by_keyword("wireless headphones", limit=100)
    """
    inputs = [{"keyword": keyword}]
    snapshot_id = trigger_collection(inputs, limit=limit, **kwargs)
    return get_results(snapshot_id)


def discover_by_category(category_url: str, limit: int = 100, **kwargs) -> list[dict]:
    """
    Discover all products from a Zepto category page.

    Example:
        results = discover_by_category("https://zeptonow.com/s?k=headphones", limit=200)
    """
    inputs = [{"url": category_url}]
    snapshot_id = trigger_collection(inputs, limit=limit, **kwargs)
    return get_results(snapshot_id)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Example 1: Track specific product URLs ─────────────────────────────────
    print("\n===== Example 1: Track by URL =====")
    sample_urls = [
        "https://www.zeptonow.com/products/sample-product",
        # Add more Zepto product URLs here
    ]
    results = track_prices(sample_urls)

    output_file = "zepto_prices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} record(s) to {output_file}")

    if results:
        r = results[0]
        title = r.get("title", r.get("name", "N/A"))
        price = r.get("final_price", r.get("price", "N/A"))
        currency = r.get("currency", "")
        available = r.get("in_stock", r.get("availability", "N/A"))
        print(f"  Sample → {title} | {price} {currency} | in_stock={available}")

    # ── Example 2: Keyword search ──────────────────────────────────────────────
    # print("\n===== Example 2: Keyword search =====")
    # kw_results = discover_by_keyword("example product", limit=20)
    # print(f"Found {len(kw_results)} products for keyword search")

    # ── Example 3: Category discovery ─────────────────────────────────────────
    # print("\n===== Example 3: Category browse =====")
    # cat_results = discover_by_category("https://zeptonow.com/category/sample", limit=50)
    # print(f"Found {len(cat_results)} products from category")
