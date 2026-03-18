# Job Scraper Assignment - Tools & Techniques for DS

## Prerequisites
- Python 3.8+
- Chrome browser installed
- All deps: `pip install -r requirements.txt` (includes selenium, scrapy, pandas, matplotlib)

**ChromeDriver Setup** (auto via webdriver-manager):
```
pip install webdriver-manager
```
(Collector.py updated to use it – no manual download.)

**Virtualenv recommended**:
```
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

## Quick Start (from project root: job-scraper-assignment/)
1. Clear old data: `rm data/raw/job_links.csv data/final/*` or manually delete
2. Collect links: `python selenium/collector.py`
3. Parse jobs: `cd scrapy_project && scrapy crawl jobs -o ../data/final/jobs.json -o ../data/final/jobs.csv`
4. Analyze: `cd .. && python analysis/analyze.py` (prints stats, saves plots/summary_charts.png)

Expected: 50-100 real jobs from Uber/Shopify/DoorDash (search: \"software engineer\", filter: Remote/US).

## Targets
- Uber: https://boards.greenhouse.io/uber
- Shopify: https://boards.greenhouse.io/shopify
- DoorDash: https://boards.greenhouse.io/doordash

## Troubleshooting
- Selenium fails? Check Chrome version, try non-headless (`headless=False`).
- No links? Sites changed – inspect HTML.
- Scrapy empty? Verify job_links.csv has valid URLs.
- Charts? `pip install matplotlib` if missing.

## Project Structure
```
job-scraper-assignment/
├── selenium/collector.py     # Link collection (dynamic JS sites)
├── scrapy_project/           # Job parsing spider
├── data/raw/job_links.csv
├── data/final/jobs.{csv,json}
├── analysis/analyze.py       # Pandas/Matplotlib trends
├── docs/report.md            # Findings
├── requirements.txt
└── README.md
```

## Outputs
- Console: Top companies/locations/skills/entry-level %
- plots/summary_charts.png
- See report.md for insights.

## Ethical Notes
- Public data only
- DOWNLOAD_DELAY=2s, robots.txt obeyed
- No auth/bots disallowed pages

## Git Workflow
- main: stable releases
- develop: integration
- feature/blackboxai-*: tasks (this via BB)
- PRs for review/merge

See /docs/report.md for analysis.

