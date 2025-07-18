import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid

# Simulated data
total_leads = 274
token_used = 0
token_limit = 5
subscription_plan = "Free Plan"
subscription_end = "6/30/2025"

# Dummy lead table
lead_data = pd.DataFrame({
    "Company": ["Metro Infusion Center", "Gentle Dental", "Inter Valley Health Plan", "Home Instead", "ATEI", "Westborn Gun Shop"],
    "Website": ["metroinfusioncenter.com", "epicdds.com", "ivhp.com", "zee.homeinstead.com.au", "onedream.house", "westborngunshop.com"],
    "Industry": ["Medical Centers", "Dentist", "Health Insurance", "Hospital/Healthcare", "Gun Store", "Gun Store"],
    "Product/Service Category": [
        "psoriatic arthritis treatment...", "senior living, assisted living...", 
        "medicare, medicare advantage...", "home care services, aged care...", 
        "No keywords found", "Specialties not mentioned"
    ],
    "Business Type (B2B, B2C)": ["B2C", "B2C", "B2C", "B2C", "N/A", "B2C"],
    "Employees": [132, 619, 102, 2352, 13, 14]
})

industry_counts = lead_data['Industry'].value_counts().reset_index()
industry_counts.columns = ['Industry', 'Count']

city_data = pd.DataFrame({
    "City": ["Brighton", "Upland", "Ukiah", "Stockton", "Institute"],
    "Count": [23, 19, 13, 11, 9]
})

weekly_trend = pd.DataFrame({
    "Date": pd.date_range(start="2025-06-01", periods=10),
    "Leads": [10, 14, 22, 38, 71, 145, 32, 28, 35, 41]
})

# --- UI Styling ---
st.set_page_config(page_title="SaaSquatch Dashboard", layout="wide")
st.markdown("<h2 style='text-align: center;'>Hi, developer! Are you ready to scrape?</h2>", unsafe_allow_html=True)

# --- Top Metrics ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Leads Scraped", total_leads)
with col2:
    st.metric("Token Usage", f"{token_used}/{token_limit}", help="0% used this month")
with col3:
    st.markdown(f"**Subscription**: {subscription_plan}")
    st.button("Upgrade")
    st.caption(f"Active until {subscription_end}")

# --- Charts ---
chart1, chart2, chart3 = st.columns(3)

with chart1:
    fig = px.pie(industry_counts, values="Count", names="Industry", title="Industry Distribution")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    fig2 = px.bar(city_data, x="City", y="Count", title="Companies by City")
    st.plotly_chart(fig2, use_container_width=True)

with chart3:
    fig3 = px.line(weekly_trend, x="Date", y="Leads", title="Weekly Growth Trend")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- Scraping History Table ---
st.markdown("### 🕵️ Scraping History")
st.text_input("Search history...", placeholder="Type to filter...")

AgGrid(lead_data, theme='dark', fit_columns_on_grid_load=True)
