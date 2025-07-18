# Saasquatch-enhancer

Lead generation tool for the Caprae AI-Readiness Challenge

This tool simulates a lightweight lead generation process by scraping Google search results for LinkedIn profiles, enriching them with email addresses (using simulated logic), and exporting them in a CRM-compatible CSV format.

---

##  Features

-  Scrapes Google search results for targeted LinkedIn profiles
-  Extracts names and LinkedIn URLs from the search data
-  Enriches results with dummy (realistic) email addresses
-  Interactive Streamlit UI (`app.py`) with keyword input + CSV export
-  Outputs a clean, structured `leads.csv` file
-  Built for quick prototyping and demonstration
-  Output is CRM-ready for use with Salesforce, HubSpot, Zoho, etc.

---

##  Project Files

| File                         | Description                                                 |
|------------------------------|-------------------------------------------------------------|
| `saasquatch_enhancer_.ipynb` | Main Colab notebook (scraper + enrichment logic)            |
| `leads.csv`                  | Generated leads output (Name, Email, LinkedIn URL)          |
| `caprae_project_report.ipynb`| Report notebook (PDF )    |
| `README.md`                  | Project overview and structure                              |
| `app.py`                     | Streamlit UI – Enter keyword, view leads, export CSV     |


---

## 🔄 Future Improvements

- Add filtering options for job title, region, or industry
- Integrate real-time API enrichment (e.g., Hunter.io, Clearbit)
- Add CRM integration (export directly to Salesforce, HubSpot, Zoho)
- Add lead deduplication and validation mechanisms

---


## 📺 Live Demo (Streamlit UI)

👉 [Click here to try the app](https://swathypk93-saasquatch-enhancer-app.streamlit.app/)

Use the dropdowns to filter leads by job title, region, or industry. Click "Download" to export.

## 👤 Author

Swathy

- Add CRM integration (export directly to tools like Salesforce, HubSpot, Zoho)


