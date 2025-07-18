import streamlit as st
import pandas as pd

# Dummy scraper function
def scrape_leads(keyword):
    # Simulated dummy data
    data = {
        "Name": ["James Doe", "Jane Smith", "Alex Johnson"],
        "Email": ["james@example.com", "jane@example.com", "alex@example.com"],
        "LinkedIn URL": [
            f"https://linkedin.com/in/{keyword.lower().replace(' ', '')}1",
            f"https://linkedin.com/in/{keyword.lower().replace(' ', '')}2",
            f"https://linkedin.com/in/{keyword.lower().replace(' ', '')}3"
        ]
    }
    return pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="SaaSquatch Lead Generator", page_icon="📊")

st.title("🦄 SaaSquatch Lead Generator")
st.markdown("Enter a search keyword (e.g., 'CTOs in India') to simulate lead scraping.")

# Input box
keyword = st.text_input("🔍 Enter Keyword:", "")

# Trigger scraping
if st.button("Generate Leads"):
    if keyword:
        leads_df = scrape_leads(keyword)
        st.success("Leads generated successfully!")
        st.dataframe(leads_df)

        # CSV download
        csv = leads_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="leads.csv",
            mime='text/csv',
        )
       ## Added app.py for Streamlit UI

    else:
        st.warning("Please enter a keyword to begin.")

