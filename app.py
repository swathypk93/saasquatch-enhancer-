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
                "Industry": "Unknown",
                "Product/Service Category": "Unknown",
                "Business Type (B2B, B2C)": "B2B",
                "Employees": "N/A"
            })
        if len(leads) >= count:
            break

    return pd.DataFrame(leads)

# ----------- Initialize Session State -----------
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Company", "Website", "Industry", "Product/Service Category", "Business Type (B2B, B2C)", "Employees"
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

# ----------- Charts Section -----------
if not st.session_state.history.empty:
    df = st.session_state.history

    col_pie, col_bar, col_line = st.columns(3)

    with col_pie:
        pie_data = df['Business Type (B2B, B2C)'].value_counts().reset_index()
        pie_data.columns = ['Type', 'Count']
        fig_pie = px.pie(pie_data, values='Count', names='Type', title="Business Type Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        df['Company Short'] = df['Compan]()
