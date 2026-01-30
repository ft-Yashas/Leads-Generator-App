from scraper import scrape_emails

url = "https://www.freshworks.com"

emails = scrape_emails(url)

print("Found Emails:")
print(emails)
