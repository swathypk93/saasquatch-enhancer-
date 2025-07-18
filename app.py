import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("scraping_history.csv")

# Title
st.markdown("<h1 style='color:#ffffff;'>🧠 Scraping History Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Use search or filters to explore scraped company data.", unsafe_allow_html=True)

# Search bar
search_term = st.text_input("🔎 Search history...", "")

# Apply search
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# Table filters
col1, col2 = st.columns(2)
with col1:
    selected_industry = st.selectbox("🏢 Filter by Industry", ["All"] + sorted(df["Industry"].dropna().unique().tolist()))
with col2:
    selected_type = st.selectbox("📊 Filter by Business Type", ["All"] + sorted(df["Business Type"].dropna().unique().tolist()))

if selected_industry != "All":
    df = df[df["Industry"] == selected_industry]

if selected_type != "All":
    df = df[df["Business Type"] == selected_type]

# Style table
def style_row(val):
    if len(str(val)) > 60:
        return val[:60] + "..."
    return val

styled_df = df.copy()
styled_df["Product/Service Category"] = styled_df["Product/Service Category"].apply(style_row)

# Show results
st.success(f"{len(styled_df)} results found.")
st.dataframe(styled_df, use_container_width=True)

# Download button
st.download_button(
    label="⬇️ Download Filtered Results",
    data=styled_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_scraping_history.csv",
    mime="text/csv"
)
