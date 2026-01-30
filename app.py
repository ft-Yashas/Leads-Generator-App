import streamlit as st
import asyncio
from discovery import search_companies
from scraper import scrape_emails_bulk
from exporter import export_to_excel

st.set_page_config(page_title="LeadGen", layout="wide")

st.title("Corporate Lead Generator")
st.write("Multi-country automated business lead system")

countries = ["India", "USA", "UK", "Canada", "Australia"]

col1, col2, col3 = st.columns(3)

with col1:
    city = st.text_input("City")

with col2:
    industry = st.text_input("Industry")

with col3:
    country = st.selectbox("Country", countries)

limit = st.number_input("Number of companies", min_value=5, max_value=100, value=20)

batch_size = 20

if "progress_index" not in st.session_state:
    st.session_state.progress_index = 0

if st.button("Generate Leads"):

    with st.spinner("Finding companies..."):
        companies = search_companies(city, industry, country, limit=limit)

    total = len(companies)

    all_leads = []

    progress_bar = st.progress(0)

    for i in range(0, total, batch_size):

        batch = companies[i:i+batch_size]

        websites = [c["website"] for c in batch]

        email_results = asyncio.run(scrape_emails_bulk(websites))

        for company in batch:

            emails = email_results.get(company["website"], [])

            lead = {
                "Company Name": company["name"],
                "Industry": company["category"],
                "City": city,
                "Country": country,
                "Address": company["address"],
                "Phone": company["phone"],
                "Website": company["website"],
                "Emails": ", ".join(emails)
            }

            all_leads.append(lead)

        progress_bar.progress(min((i + batch_size) / total, 1.0))

    file_name = export_to_excel(all_leads)

    st.success("Lead generation completed")

    st.dataframe(all_leads)

    with open(file_name, "rb") as file:
        st.download_button(
            "Download Excel File",
            file,
            file_name="leads.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
