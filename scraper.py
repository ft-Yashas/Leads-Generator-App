import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_domain(url):
    ext = tldextract.extract(url)
    return ext.domain + "." + ext.suffix


async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
    except:
        return None


def extract_emails(html):
    return set(re.findall(EMAIL_REGEX, html))


def extract_mailtos(soup):
    emails = set()
    for link in soup.select("a[href^=mailto]"):
        email = link.get("href").replace("mailto:", "").split("?")[0]
        emails.add(email)
    return emails


def find_contact_page(base_url, soup):
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        if "contact" in href or "about" in href:
            return urljoin(base_url, link["href"])
    return None


async def scrape_single_site(session, website):
    emails_found = set()

    html = await fetch(session, website)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    emails_found |= extract_emails(html)
    emails_found |= extract_mailtos(soup)

    contact_url = find_contact_page(website, soup)

    if contact_url:
        contact_html = await fetch(session, contact_url)
        if contact_html:
            contact_soup = BeautifulSoup(contact_html, "html.parser")
            emails_found |= extract_emails(contact_html)
            emails_found |= extract_mailtos(contact_soup)

    domain = get_domain(website)

    clean = []
    for email in emails_found:
        if domain in email:
            clean.append(email)

    return list(set(clean))


async def scrape_emails_bulk(websites):
    results = {}

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:

        tasks = []
        for site in websites:
            tasks.append(scrape_single_site(session, site))

        responses = await asyncio.gather(*tasks)

        for i in range(len(websites)):
            results[websites[i]] = responses[i]

    return results
