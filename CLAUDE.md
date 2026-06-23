# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: CloudAbacus (运算盘)

GPU cloud pricing aggregator — scrapes hourly pricing from 40+ global GPU cloud platforms, plus GPU rental/compute-futures news from Google News RSS. All output is written as JS variable files consumed by a frontend dashboard.

## Commands

```bash
# Full price scrape (requests mode — fast, static pages only)
python fetch_prices.py

# Full price scrape with Playwright (SPA pages, required for GitHub Actions)
python fetch_prices.py --playwright

# Quick mode: top-5 platforms only
python fetch_prices.py --quick

# Vast.ai only (high-frequency, lightweight)
python fetch_prices.py --vast-only

# News scrapers
python fetch_news.py        # GPU rental news → news.js
python fetch_futures.py     # Compute futures news → futures_news.js

# Vast.ai historical data extractor
python extract_vast_history.py

# Install all dependencies (including Playwright browser)
pip install requests beautifulsoup4 playwright feedparser deep-translator
playwright install chromium
```

## Architecture

### Price scraping pipeline (`fetch_prices.py`)

The main scraper (~2283 lines). Three-tier architecture:

1. **Scraper functions** — Each platform has a dedicated function (e.g., `scrape_vast()`, `scrape_runpod()`, `scrape_lambda()`). Complex platforms get custom logic; simpler ones use `scrape_generic()`.
2. **Platform registry** — `CORE_PLATFORMS` (8 high-priority) + `EXTENDED_PLATFORMS` (~40) define `(name, url, needs_playwright)` tuples. A `custom_scrapers` dict maps platform names to `(requests_fn, playwright_fn)` tuples for platforms needing special handling.
3. **Multi-strategy extraction** — Falls through 4 strategies: regex on HTML text → HTML `<table>` rows → JSON-LD structured data → Next.js `__NEXT_DATA__`. Price validation via `PRICE_RANGES` per GPU model.

**Key design decisions:**

- All prices normalized to **USD/hour**. EUR prices converted at 1.08 rate; CNY monthly prices divided by 730 hours and CNY→USD at 0.14.
- GPU names normalized through `normalize_gpu_name()` / `COMMON_GPUS` regex list — maps raw platform names to standard labels like `"NVIDIA H100 (80GB SXM)"`.
- Output files use `atomic_write_js()` (write to `.tmp` then `Path.replace()`) to avoid corruption during concurrent reads.
- `scrape_with_playwright()` is the shared Playwright worker: launches headless Chromium, dismisses cookie banners, scrolls for lazy-loaded content, extracts both inner text and inner HTML.

### Output files

| File                 | Variable              | Content                                                                                     |
| -------------------- | --------------------- | ------------------------------------------------------------------------------------------- |
| `pricing_live.js`    | `GPU_PRICING_LIVE`    | Latest scraped prices grouped by GPU model                                                  |
| `price_history.js`   | `PRICE_HISTORY_DATA`  | Compact snapshots `{ts, d: {gpu: {platform: price}}}` — used by charts, kept 1000 snapshots |
| `pricing_history.js` | `GPU_PRICING_HISTORY` | Full-format snapshots with all metadata — kept 168 snapshots (1 week hourly)                |
| `price_history.json` | —                     | JSON backup of `PRICE_HISTORY_DATA`                                                         |
| `news.js`            | `GPU_NEWS`            | GPU rental market news (50 articles max, translated CN↔EN)                                  |
| `futures_news.js`    | `GPU_NEWS`            | GPU compute futures news (50 articles max)                                                  |

### News scrapers (`fetch_news.py`, `fetch_futures.py`)

Both follow the same pipeline:

1. Google News RSS → get titles/sources/dates
2. Relevance filter (must hit both rental/compute keyword sets AND futures/compute keyword sets respectively)
3. English articles → Google Translate to Chinese (`deep-translator`)
4. Merge with existing output (dedup by title, keep newest 50, sort by date descending)
5. Build rich fallback content when full text unavailable

### `_availability.py`

Imported by `fetch_prices.py`. Queries Vast.ai's public API (`console.vast.ai/api/v0/bundles/`) to get per-GPU rental scale stats (total machines, total GPUs, rented count, rentable count). Results appended to pricing entries as `availability` field.

### `extract_vast_history.py`

Playwright-based deep scraper for Vast.ai historical data. Intercepts network responses for API calls, extracts embedded JSON (`__NEXT_DATA__`, inline bundles), and reads from existing `pricing_live.js` as fallback. Appends today's snapshot to `price_history.js`.

### GitHub Actions (`.github/workflows/daily-scrape.yml`)

Runs hourly at UTC :15. Installs all deps including Playwright chromium, runs `fetch_prices.py --playwright`, then both news scrapers (continue-on-error), commits changed output files and pushes.

## Important notes

- **AutoDL is disabled** in the platform registry — it blocks non-China IPs and won't work from GitHub Actions runners.
- `test_sina.py` is a debugging script for testing Sina Finance article extraction — not part of the main pipeline.
- The project root contains helper files like `_page.html`, `_api_live.json`, `vast_screenshot.png` etc. — these are transient debug artifacts, not tracked in git.
- `GPU Rental Market List.json` is a reference catalog of ~75 GPU platforms — used for documentation, not consumed by scrapers.
- **Windows encoding**: The preamble `sys.stdout = io.TextIOWrapper(...)` in every script fixes GBK encoding issues on Windows. Do not remove it.
- Scrapers support `HTTP_PROXY`/`HTTPS_PROXY` env vars for running behind a proxy.
