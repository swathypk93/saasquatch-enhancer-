import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import requests
from bs4 import BeautifulSoup
import time
import re

# ----------- Real Web Scraping Logic (Google Search + LinkedIn filter) -----------
def scrape_leads(query, count=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}+site:linkedin.com/in"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    leads = []
    for link in links:
        href = link['href']
        match = re.search(r'https://www\.linkedin\.com/in/[^&]+', href)
        if match:
            name = link.get_text().strip()
            leads.append({
                "Company": name[:30] if name else "LinkedIn User",
                "Website": match.group(0),
                "Industry": "SaaS",
                "Product/Service Category": "Software",
                "Business Type (B2B, B2C)": "B2B",
                "Employees": "50",
                "Title": "CEO",
                "Region": "California"
            })
        if len(leads) >= count:
            break

    return pd.DataFrame(leads)

# ----------- Initialize Session State -----------
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Company", "Website", "Industry", "Product/Service Category",
        "Business Type (B2B, B2C)", "Employees", "Title", "Region"
    ])
if 'total_leads' not in st.session_state:
    st.session_state.total_leads = 0

# ----------- App UI -----------
st.set_page_config(page_title="SaaSquatch Enhancer", layout="wide")
st.markdown("<h2 style='text-align: center;'>Hi, developer! Are you ready to scrape?</h2>", unsafe_allow_html=True)

# ----------- Input Form -----------
with st.form("scrape_form"):
    st.markdown("### 🔍 Enter a keyword, company or domain to generate leads")
    query = st.text_input("Enter search term")
    num_results = st.slider("Number of leads", 1, 20, 5)
    submitted = st.form_submit_button("Search")

# ----------- Scraping Execution -----------
if submitted and query:
    with st.spinner("🔍 Scraping LinkedIn leads from Google..."):
        new_leads = scrape_leads(query, num_results)
        st.session_state.history = pd.concat([st.session_state.history, new_leads], ignore_index=True)
        st.session_state.total_leads += len(new_leads)
    st.success(f"✅ {len(new_leads)} leads added to dashboard!")

# ----------- Metric Cards -----------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Leads Scraped", st.session_state.total_leads)
with col2:
    tokens_used = st.session_state.total_leads // 5
    st.metric("Token Usage", f"{tokens_used}/5", help="1 token per 5 leads")
with col3:
    st.markdown("**Subscription**: Free Plan")
    st.button("Upgrade")
    st.caption("Active until 6/30/2025")

# ----------- Charts & Filters -----------
if not st.session_state.history.empty:
    df = st.session_state.history

    # --- FILTERS ---
    st.markdown("### 🎯 Filter Leads")
    titles = df['Title'].dropna().unique()
    regions = df['Region'].dropna().unique()
    industries = df['Industry'].dropna().unique()

    selected_titles = st.multiselect("Filter by Job Title", titles)
    selected_regions = st.multiselect("Filter by Region", regions)
    selected_industries = st.multiselect("Filter by Industry", industries)

    filtered_df = df.copy()
    if selected_titles:
        filtered_df = filtered_df[filtered_df['Title'].isin(selected_titles)]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_industries:
        filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]

    # --- Charts ---
    col_pie, col_bar, col_line = st.columns(3)

    with col_pie:
        pie_data = filtered_df['Business Type (B2B, B2C)'].value_counts().reset_index()
        pie_data.columns = ['Type', 'Count']
        fig_pie = px.pie(pie_data, values='Count', names='Type', title="Business Type Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        filtered_df['Company Short'] = filtered_df['Company'].str.extract(r'(\w+)')
        bar_data = filtered_df['Company Short'].value_counts().reset_index()
        bar_data.columns = ['Company', 'Count']
        fig_bar = px.bar(bar_data, x='Company', y='Count', title="Company Name Frequency")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_line:
        trend = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=len(filtered_df)),
            "Leads": list(range(1, len(filtered_df) + 1))
        })
        fig_line = px.line(trend, x='Date', y='Leads', title="Lead Growth Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # ----------- Table + Download -----------
    st.markdown("### 🧾 Scraping History")
    AgGrid(filtered_df.drop(columns=['Company Short'], errors='ignore'), theme="dark", fit_columns_on_grid_load=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Leads", data=csv, file_name="leads.csv", mime="text/csv")

else:
    st.info("No leads yet. Use the form above to begin.")


   
