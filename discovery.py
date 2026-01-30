import requests
import time
import os




try:
    import streamlit as st
    SERP_API_KEY = st.secrets.get("SERP_API_KEY")
except:
    SERP_API_KEY = os.getenv("SERP_API_KEY")

BASE_URL = "https://serpapi.com/search.json"







def expand_industry(industry):

    industry = industry.strip()

    variations = set()

    variations.add(industry)
    variations.add(f"{industry} Company")
    variations.add(f"{industry} Services")
    variations.add(f"{industry} Firm")
    variations.add(f"{industry} Provider")

    return list(variations)










def expand_city(city):

    city = city.strip()

    zones = [
        "CBD",
        "Downtown",
        "Business Park",
        "Industrial Area",
        "Commercial Area",
        "Tech Park",
        "Corporate Park",
        "Financial District"
    ]

    expanded = [city]

    for zone in zones:
        expanded.append(f"{zone} {city}")

    return expanded









def search_companies(city, industry, country, limit=50):

    if not SERP_API_KEY:
        raise Exception("SERP_API_KEY not found. Add it to environment variables or Streamlit secrets.")

    industry_variants = expand_industry(industry)
    location_variants = expand_city(city)

    final_results = []

    seen_websites = set()
    seen_names = set()

    for industry_term in industry_variants:

        for location in location_variants:

            query = f"{industry_term} in {location} {country}"

            next_page_token = None

            while len(final_results) < limit:

                params = {
                    "engine": "google_maps",
                    "q": query,
                    "type": "search",
                    "api_key": SERP_API_KEY
                }

                if next_page_token:
                    params["next_page_token"] = next_page_token

                try:
                    response = requests.get(BASE_URL, params=params, timeout=30)
                    data = response.json()
                except Exception as e:
                    print("Request error:", e)
                    break

                local_results = data.get("local_results", [])

                if not local_results:
                    break

                for place in local_results:

                    name = place.get("title", "")
                    website = place.get("website", "")
                    normalized_name = name.lower().strip()

                    # Deduplication
                    if website and website in seen_websites:
                        continue

                    if normalized_name in seen_names:
                        continue

                    company = {
                        "name": name,
                        "address": place.get("address"),
                        "phone": place.get("phone"),
                        "website": website,
                        "category": place.get("type")
                    }

                    final_results.append(company)

                    if website:
                        seen_websites.add(website)

                    seen_names.add(normalized_name)

                    if len(final_results) >= limit:
                        break

                pagination = data.get("serpapi_pagination", {})
                next_page_token = pagination.get("next_page_token")

                if not next_page_token:
                    break

                # Delay required for Google Maps pagination
                time.sleep(3)

            if len(final_results) >= limit:
                break

        if len(final_results) >= limit:
            break

    return final_results
