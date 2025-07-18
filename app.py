import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import time

# --- Dummy Lead Scraper (Replace this with real API/scraping logic) ---
def scrape_leads(query, count=5):
    time.sleep(2)  # simulate scraping delay
    leads = []
    for i in range(count):
        leads.append({
            "Company": f"{query.title()} Inc {i+1}",
            "Website": f"https://{query}{i+1}.com",
            "Industry": "Tech",
            "Product/Service Category": "SaaS Tools",
            "Business Type (B2B, B2C)": "B2B",
            "Employees": 100 + i * 20
        })
    return pd.DataFrame(leads)

# --- Session State Initialization ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Company", "Website", "Industry", "Product/Service Category", "Business Type (B2B, B2C)", "Employees"
    ])
if 'total_leads' not in st.session_state:
    st.session_state.total_leads = 0

# --- App Config & Header ---
st.set_page_config(page_title="SaaSquatch Enhancer", layout="wide")
st.markdown("<h2 style='text-align: center;'>Hi, developer! Are you ready to scrape?</h2>", unsafe_allow_html=True)

# --- Scrape Input Form ---
with st.form("scrape_form"):
    st.markdown("### 🔍 Enter a keyword, domain or company to generate leads")
    query = st.text_input("Enter search term")
    num_results = st.slider("Number of leads", 1, 20, 5)
    submit = st.form_submit_button("Search")

# --- Perform Scraping ---
if submit and query:
    with st.spinner("Scraping leads..."):
        new_leads = scrape_leads(query, num_results)
        st.session_state.history = pd.concat([st.session_state.history, new_leads], ignore_index=True)
        st.session_state.total_leads += len(new_leads)
    st.success(f"✅ Added {len(new_leads)} new leads!")

# --- Dashboard Metrics ---
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

# --- Visual Charts Section ---
if not st.session_state.history.empty:
    pie_col, bar_col, line_col = st.columns(3)

    # Pie: Industry Distribution
    with pie_col:
        pie_data = st.session_state.history['Industry'].value_counts().reset_index()
        pie_data.columns = ['Industry', 'Count']
        fig = px.pie(pie_data, values='Count', names='Industry', title="Industry Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Bar: Companies by Name
    with bar_col:
        comp_counts = st.session_state.history['Company'].str.extract(r'(\w+) Inc')[0].value_counts().reset_index()
        comp_counts.columns = ['Company', 'Count']
        fig2 = px.bar(comp_counts, x='Company', y='Count', title="Companies by Name")
        st.plotly_chart(fig2, use_container_width=True)

    # Line: Weekly Trend (Fake Date-based Trend)
    with line_col:
        trend_df = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=len(st.session_state.history)),
            "Leads": [1] * len(st.session_state.history)
        })
        fig3 = px.line(trend_df, x="Date", y="Leads", title="Weekly Growth Trend")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🧾 Scraping History")
    AgGrid(st.session_state.history, theme="dark", fit_columns_on_grid_load=True)

    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Leads", data=csv, file_name="leads.csv", mime="text/csv")
else:
    st.info("No leads scraped yet. Enter a query above to begin.")


