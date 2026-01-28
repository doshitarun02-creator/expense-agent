import streamlit as st
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import PIL.Image
import json
import re
import pandas as pd
import plotly.express as px
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI CFO Agent", page_icon="📈", layout="wide")

# --- API KEYS ---
GEMINI_KEY = "AIzaSyBriYn4tDHgjZIVarhlHm-oZReGnzZkF10"  # <--- PASTE KEY HERE

# --- SETUP ---
@st.cache_resource
def get_db_connection():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open("Expense_Tracker").sheet1

# --- AI FUNCTIONS ---
def extract_receipt_data(image_file):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    img = PIL.Image.open(image_file)
    prompt = """
    Analyze receipt. Return ONLY raw JSON:
    {"date": "YYYY-MM-DD", "store": "Store Name", "category": "Category", "total": "Amount (number only)", "summary": "Short description"}
    """
    response = model.generate_content([prompt, img])
    clean_text = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(clean_text)

def process_bulk_csv(csv_text):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a Data Cleaning AI. I have a raw bank statement. 
    Your job:
    1. Identify the 'Date', 'Description', and 'Amount'.
    2. Categorize each transaction (e.g., Food, Travel, Tech, Salary).
    3. Ignore 'Salary' or positive income (we only track expenses).
    4. Return valid JSON list.

    RAW DATA:
    {csv_text}

    OUTPUT FORMAT (JSON List):
    [
      {{"date": "YYYY-MM-DD", "store": "Clean Name", "category": "Category", "total": "Amount", "summary": "Desc"}},
      ...
    ]
    """
    response = model.generate_content(prompt)
    clean_text = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(clean_text)

def get_ai_advice(df):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    summary = df.groupby('Category')['Amount'].sum().to_string()
    total = df['Amount'].sum()
    prompt = f"Act as a CFO. Total Spent: ₹{total}. Breakdown: {summary}. Give 3 ruthless tips to save money."
    response = model.generate_content(prompt)
    return response.text

# --- MAIN UI ---
st.title("📈 AI Financial Command Center")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["🧾 Receipt Scanner", "📂 Bulk Upload (CSV)", "📊 CFO Dashboard"])

# --- TAB 1: Single Receipt ---
with tab1:
    st.header("Upload Single Receipt")
    uploaded_file = st.file_uploader("Drop image here...", type=["jpg", "png", "jpeg"])
    if uploaded_file and st.button("Process Receipt"):
        with st.spinner("Scanning..."):
            try:
                data = extract_receipt_data(uploaded_file)
                sheet = get_db_connection()
                sheet.append_row([data['date'], data['store'], data['category'], float(data['total']), data['summary']])
                st.success("Receipt Saved!")
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: Bulk CSV ---
with tab2:
    st.header("Upload Bank Statement")
    csv_file = st.file_uploader("Upload CSV (Date, Description, Amount)", type=["csv"])
    
    if csv_file:
        # Show preview
        df_preview = pd.read_csv(csv_file)
        st.dataframe(df_preview.head())
        
        if st.button("🚀 Process Bulk Data"):
            with st.spinner("AI is reading all rows..."):
                try:
                    # Convert CSV to string for AI
                    csv_text = df_preview.to_string(index=False)
                    
                    # Get AI to clean it
                    ai_data = process_bulk_csv(csv_text)
                    st.success(f"AI identified {len(ai_data)} valid expenses!")
                    
                    # Push to Google Sheets
                    sheet = get_db_connection()
                    for item in ai_data:
                        row = [item['date'], item['store'], item['category'], float(item['total']), item['summary']]
                        sheet.append_row(row)
                        
                    st.balloons()
                    st.toast("Batch upload complete!")
                    
                except Exception as e:
                    st.error(f"Error processing CSV: {e}")

# --- TAB 3: Dashboard ---
with tab3:
    try:
        sheet = get_db_connection()
        records = sheet.get_all_records()
        if records:
            df = pd.DataFrame(records)
            
            # Metrics
            total = df['Amount'].sum()
            c1, c2 = st.columns(2)
            c1.metric("Total Spend", f"₹{total:,.0f}")
            c2.metric("Tx Count", len(df))
            
            # Charts
            col1, col2 = st.columns([2,1])
            with col1:
                fig = px.bar(df, x='Category', y='Amount', color='Category')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                if st.button("Get CFO Advice"):
                    advice = get_ai_advice(df)
                    st.info(advice)
    except:
        st.write("No data yet.")