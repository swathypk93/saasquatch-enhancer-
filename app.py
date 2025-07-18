import streamlit as st
import pandas as pd

# --------------------------
# Sample lead data (dummy)
# --------------------------
sample_data = pd.DataFrame({
    "Name": ["John Doe", "Jane Smith", "Alex Johnson", "Priya Mehta", "Suresh Reddy"],
    "Email": ["john@ex.com", "jane@ex.com", "alex@ex.com", "priya@ex.com", "suresh@ex.com"],
    "Job Title": ["CTO", "Marketing Manager", "CEO", "CTO", "Data Scientist"],
    "Region": ["India", "USA", "India", "UK", "India"],
    "Industry": ["Tech", "Retail", "Finance", "Tech", "AI"],
    "LinkedIn URL": [
        "https://linkedin.com/in/john",
        "https://linkedin.com/in/jane",
        "https://linkedin.com/in/alex",
        "https://linkedin.com/in/priya",
        "https://linkedin.com/in/suresh"
    ]
})

# --------------------------
# Streamlit App UI
# --------------------------
st.set_page_config(page_title="Lead Generator with Filters", page_icon="🦄")
st.title("🦄 SaaSquatch Lead Generator")
st.markdown("Use filters to find and download leads by title, region, and industry.")

# --------------------------
# Filter Widgets
# --------------------------
job_filter = st.selectbox("🔧 Filter by Job Title:", options=["All"] + sorted(sample_data["Job Title"].unique())), st.selectbox("🌎 Filter by Region:", options=["All"] + sorted(sample_data["Region"].unique())), st.selectbox("🏢 Filter by Industry:", options=["All"] + sorted(sample_data["Industry"].unique()))

# --------------------------
# Apply Filters
# --------------------------
filtered_data = sample_data.copy()
if job_filter != "All":
    filtered_data = filtered_data[filtered_data["Job Title"] == job_filter]
if region_filter != "All":
    filtered_data = filtered_data[filtered_data["Region"] == region_filter]
if industry_filter != "All":
    filtered_data = filtered_data[filtered_data["Industry"] == industry_filter]

# --------------------------
# Show + Download Results
# --------------------------
if not filtered_data.empty:
    st.success(f"{len(filtered_data)} leads found.")
    st.dataframe(filtered_data)

    # Download CSV
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Leads",
        data=csv,
        file_name="filtered_leads.csv",
        mime='text/csv',
    )
else:
    st.warning("No leads match the selected filters.")


