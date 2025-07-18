import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import time

# Simulate scraping from query
def scrape_leads(query, count=5):
    time.sleep(2)  # simulate delay
    leads = []
    for i in range(count):
        leads.append({
            "Company": f"{query.title()} Inc {i+1}",
            "Website": f"https://{query}{i+1}.com",
            "Industry": "Tech",
            "Product/Service Category": "Software, SaaS",
            "Business Type (B2B, B2C)": "B2B",
            "Employees": 50 + i * 10
        })
    return pd.DataFrame(leads)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Company", "Website", "Industry", "Product/Service Category", "Business Type (B2B, B2C)", "Employees"
    ])
if 'total_leads' not in st.session_state:
    st.session_state.total_leads = 0

# UI
st.set_page_config(page_title="SaaSquatch Live Scraper", layout="wide")
st.markdown("<h2 style='text-align: center;'>Hi, developer! Are you ready to scrape?</h2>", unsafe_allow_html=True)

# Input form
with st.form("scrape_form"):
    st.markdown("### 🔍 Enter a keyword, domain or industry to generate leads")
    query = st.text_input("Enter query")
    num_results = st.slider("Number of leads", 1, 20, 5)
    submit = st.form_submit_button("Search")

# If form is submitted
if submit and query:
    with st.spinner("Scraping leads..."):
        new_leads = scrape_leads(query, num_results)
        st.session_state.history = pd.concat([st.session_state.history, new_leads], ignore_index=True)
        st.session_state.total_leads += len(new_leads)
    st.success("✅ Leads added to dashboard!")

# --- Dashboard Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Leads Scraped", st.session_state.total_leads)
with col2:
    used_tokens = st.session_state.total_leads // 5
    st.metric("Token Usage", f"{used_tokens}/5", help="1 token per 5 leads")
with col3:
    st.markdown("**Subscription**: Free Plan")
    st.button("Upgrade")
    st.caption("Active until 6/30/2025")

# --- Charts (if data exists) ---
if not st.session_state.history.empty:
    industry_dist = st.session_state.history['Industry'].value_counts().reset_index()
    industry_dist.columns = ['Industry', 'Count']
    pie, bar, line = st.columns(3)

    with pie:
        st.plotly_chart(px.pie(industry_dist, values='Count', names='Industry', title="Industry Distribution"), use_container_width=True)
    with bar:
        st.plotly_chart(px.bar(st.session_state.history['Company'].str.extract(r'(\w+) Inc')[0].value_counts().reset_index(),
                               x='index', y=0, labels={'index': 'Company', 0: 'Count'},
                               title="Companies by Name"), use_container_width=True)
    with line:
        trend_df = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=len(st.session_state.history)),
            "Leads": [1] * len(st.session_state.history)
        })
        st.plotly_chart(px.line(trend_df, x="Date", y="Leads", title="Weekly Growth Trend"), use_container_width=True)

    st.markdown("---")
    st.markdown("### 🕵️ Scraping History")
    AgGrid(st.session_state.history, theme="dark", fit_columns_on_grid_load=True)

    # CSV download
    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Leads", data=csv, file_name="leads.csv", mime="text/csv")
else:
    st.info("No leads scraped yet. Enter a query above to begin.")

