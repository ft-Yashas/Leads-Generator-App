from discovery import search_companies

results = search_companies("Bangalore", "IT Companies")

for company in results:
    print(company)
