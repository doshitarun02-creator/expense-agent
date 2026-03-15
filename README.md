# 🚀 AI Financial CFO Agent

A full-stack AI application that automates expense tracking and provides financial strategy using Google Gemini 2.5 Flash.

### 🔗 [Live Demo](https://share.streamlit.io/YOUR_USERNAME/expense-agent) (Click to Launch)

## 📅 Development Roadmap & Milestones

This project was developed in three structured phases for the Agentic AI Workshop:

* **Week 1: Foundation & Data Pipeline:** * Engineered the Streamlit UI skeleton.
    * Established real-time cloud database synchronization using the Google Sheets API.
* **Week 2: AI Vision & Data Extraction:** * Integrated Google Gemini 2.5 Flash for unstructured receipt scanning.
    * Built the Pandas logic for bulk CSV bank statement cleaning and auto-categorization.
* **Week 3: CFO Agent & Analytics (Current MVP):** * Deployed the AI CFO logic engine to analyze spending velocity and generate cost-cutting strategies.
    * Integrated Plotly for interactive financial data visualization.

## 💡 Features
* **🧾 Receipt Scanner:** Uses **Gemini Vision** to extract data (Date, Store, Amount) from images.
* **🧠 CFO Logic:** Analyzes spending patterns and provides ruthless cost-cutting advice.
* **📂 Bulk Processing:** Upload generic bank statements (CSV) and auto-categorize transactions.
* **☁️ Cloud Database:** Syncs all data in real-time to **Google Sheets**.

## 🛠️ Tech Stack
* **AI Engine:** Google Gemini 2.5 Flash (via Google Gen AI SDK)
* **Frontend:** Streamlit (Python)
* **Database:** Google Sheets API
* **Visualization:** Plotly & Pandas

## 🚀 How to Run Locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `secrets.toml` with API keys
4. Run: `streamlit run app.py`
