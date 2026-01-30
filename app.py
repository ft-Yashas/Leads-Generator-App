import streamlit as st
import asyncio
from discovery import search_companies
from scraper import scrape_emails_bulk
from exporter import export_to_excel


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="LeadGen | Corporate Lead Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CUSTOM UI THEME ----------------

st.markdown("""
<style>

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* Main container card */
.main-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
}

/* Hero title */
.hero-title {
    text-align: center;
    font-size: 44px;
    font-weight: bold;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    color: transparent;
}

/* Subtitle */
.hero-subtitle {
    text-align: center;
    font-size: 16px;
    color: #cbd5f5;
    margin-bottom: 20px;
}

/* Button style */
div.stButton > button {
    background: linear-gradient(to right, #0ea5e9, #6366f1);
    color: white;
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

/* Metric cards */
.metric-box {
    background: rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    color: white;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: linear-gradient(to right, #0ea5e9, #6366f1);
    color: white;
    text-align: center;
    padding: 8px;
    font-size: 13px;
    z-index: 100;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HERO HEADER ----------------

st.markdown('<div class="hero-title">Corporate Leads Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Automated Business Discovery & Verified Email Extraction Platform</div>', unsafe_allow_html=True)
st.caption("Version 1.0 | India + Global Business Lead Engine")


# ---------------- SIDEBAR CONTROL PANEL ----------------

st.sidebar.title("Lead Search Panel")
st.sidebar.markdown("Configure your lead search")

city = st.sidebar.text_input("City")
industry = st.sidebar.text_input("Industry (Eg: IT Companies)")
country = st.sidebar.selectbox("Country", ["India", "USA", "UK", "Canada", "Australia"])

limit = st.sidebar.number_input("Companies Limit", min_value=5, max_value=100, value=20)

st.sidebar.markdown("---")

st.sidebar.title("Developed By : ")
st.sidebar.markdown("""
**Yashas R**    
Python Automation Project 
""")


# ---------------- MAIN PIPELINE ----------------

batch_size = 20

if st.button("Generate Leads"):

    if not city or not industry:
        st.warning("Please enter both City and Industry")
    else:

        with st.spinner("Finding companies..."):
            companies = search_companies(city, industry, country, limit=limit)

        total = len(companies)

        all_leads = []

        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        progress_bar = st.progress(0)

        for i in range(0, total, batch_size):

            batch = companies[i:i + batch_size]

            websites = [c["website"] for c in batch]

            email_results = asyncio.run(scrape_emails_bulk(websites))

            for company in batch:

                emails = email_results.get(company["website"], [])

                lead = {
                    "Company Name": company.get("name"),
                    "Industry": company.get("category"),
                    "City": city,
                    "Country": country,
                    "Address": company.get("address"),
                    "Phone": company.get("phone"),
                    "Website": company.get("website"),
                    "Emails": ", ".join(emails)
                }

                all_leads.append(lead)

            progress_bar.progress(min((i + batch_size) / total, 1.0))

        # ---------------- EXPORT ----------------

        file_name = export_to_excel(all_leads)

        st.success("✅ Lead generation completed successfully!")

        # ---------------- KPI METRICS ----------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f'<div class="metric-box">Companies<br><b>{len(all_leads)}</b></div>',
                unsafe_allow_html=True
            )

        with col2:
            total_emails = sum(1 for lead in all_leads if lead["Emails"])
            st.markdown(
                f'<div class="metric-box">Emails Found<br><b>{total_emails}</b></div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div class="metric-box">Country<br><b>{country}</b></div>',
                unsafe_allow_html=True
            )

        # ---------------- DATA PREVIEW ----------------

        st.subheader("📊 Lead Preview")
        st.dataframe(all_leads, use_container_width=True)

        # ---------------- DOWNLOAD BUTTON ----------------

        with open(file_name, "rb") as file:
            st.download_button(
                label="⬇ Download Excel File",
                data=file,
                file_name="corporate_leads.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown('</div>', unsafe_allow_html=True)


