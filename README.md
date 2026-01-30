# Corporate Lead Generator App

A Python-based web application that automatically generates business leads by discovering companies, scraping websites for verified emails, and exporting structured Excel reports.

## Features

- City + Industry based company discovery
- Multi-country support
- Automated website crawling
- Business email extraction with domain validation
- Batch processing for stability
- Excel export
- Streamlit web UI

## Tech Stack

- Python
- Streamlit
- BeautifulSoup
- Aiohttp
- Pandas
- SerpAPI

## How To Run Locally

1. Install dependencies

pip install -r requirements.txt

2. Start app

streamlit run app.py

## Output

Generates Excel file with:

- Company Name
- Industry
- City
- Country
- Address
- Phone
- Website
- Emails

## Disclaimer
This tool collects only publicly available business contact data and should be used responsibly.
