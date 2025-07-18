import streamlit as st
import pandas as pd
import time

# Dummy function (replace with actual scraper)
def generate_leads(query):
    time.sleep(2)  # Simulate processing time
    return pd.DataFrame({
        "Name": ["Alice Johnson", "Bob Smith", "Cathy Lee"],
        "Company": ["TechCorp", "DataGen", "InnovateX"],
        "Role": ["CTO", "Marketing Head", "Product Lead"],
        "Email": ["alice@techcorp.com", "bob@datagen.com", "cathy@innovatex.com"],
        "LinkedIn": [
            "https://linkedin.com/in/alice",
            "https://linkedin.com/in/bob",
            "https://linkedin.com/in/cathy"
        ]
    })

# App layout
st.set_page_config(page_title="Lead Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>🚀 Lead Generator Tool</h1>", unsafe_allow_html=True)

st.markdown("### 🔎 Enter a company name, keyword, or domain")
query = st.text_input("Search for leads")

if st.button("Search"):
    if not query:
        st.warning("Please enter a keyword to search.")
    else:
        with st.spinner("🔍 Finding leads... Please wait."):
            leads = generate_leads(query)
        st.success("✅ Leads generated successfully!")
        st.dataframe(leads, use_container_width=True)

        # CSV Download
        csv = leads.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Leads as CSV", data=csv, file_name="leads.csv", mime="text/csv")
