# 🚀 AI Financial CFO Agent

A full-stack AI application that automates expense tracking and provides financial strategy using Google Gemini 2.5 Flash.

### 🔗 [Live Demo](https://share.streamlit.io/YOUR_USERNAME/expense-agent) (Click to Launch)

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
