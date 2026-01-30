import requests

SERP_API_KEY = "127bf6852b2d590d6f8440c48f9948866ca444339a5b09956203b378b0e5a4d3"


def search_companies(city, industry, country, limit=20):
    query = f"{industry} in {city} {country}"

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": SERP_API_KEY
    }

    response = requests.get("https://serpapi.com/search.json", params=params)

    data = response.json()

    companies = []

    if "local_results" in data:
        for place in data["local_results"][:limit]:

            company = {
                "name": place.get("title"),
                "address": place.get("address"),
                "phone": place.get("phone"),
                "website": place.get("website"),
                "category": place.get("type")
            }

            if company["website"]:
                companies.append(company)

    return companies
