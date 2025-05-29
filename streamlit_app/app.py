import streamlit as st
import requests
import json
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Update with your Hugging Face FastAPI backend URL
 url = "https://nani2906-my-fastapi-backend.hf.space/ask"


st.set_page_config(page_title="🧠💬 AI Finance Assistant", layout="wide")
st.title("🧠💬 AI Finance Assistant")
st.write("Ask anything about a company's stock and get insights with voice support.")

# Country selection
country = st.selectbox("Select Country", ["United States", "India"], index=0)

# Stock options by country
stock_options = {
    "United States": {
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "Google (GOOGL)": "GOOGL",
        "Microsoft (MSFT)": "MSFT",
        "Amazon (AMZN)": "AMZN"
    },
    "India": {
        "Reliance (RELIANCE.NS)": "RELIANCE.NS",
        "TCS (TCS.NS)": "TCS.NS",
        "Infosys (INFY.NS)": "INFY.NS",
        "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS",
        "ICICI Bank (ICICIBANK.NS)": "ICICIBANK.NS"
    }
}

# Stock selection
stock_name = st.selectbox("Select Stock", list(stock_options[country].keys()))
stock_symbol = stock_options[country][stock_name]

# User query
query = st.text_input("Enter your financial question", "What is the current stock price?")

# Ask button
if st.button("Ask"):
    with st.spinner("Thinking... 🤖"):
        try:
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"query": query, "stock_symbol": stock_symbol})
            response = requests.post(API_URL, headers=headers, data=payload, timeout=90)

            if response.status_code == 200:
                result = response.json()
                st.subheader("📈 Stock Data")
                st.json(result.get("stock_data", {}))

                st.subheader("📰 Latest News")
                for news_item in result.get("news", []):
                    st.markdown(f"- {news_item}")

                st.subheader("📄 Relevant Documents")
                for doc in result.get("documents", []):
                    st.markdown(f"- {doc}")

                st.subheader("🧠 Summary")
                st.success(result.get("summary", "No summary available."))
            else:
                st.error(f"❌ API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Something went wrong: {e}")

# Optional charts
st.markdown("---")
st.subheader("📊 Stock Price Chart (Last 30 Days)")
try:
    df = yf.Ticker(stock_symbol).history(period="30d")
    if not df.empty:
        st.line_chart(df['Close'], use_container_width=True)
        st.bar_chart(df['Volume'], use_container_width=True)
    else:
        st.warning("No historical data available.")
except Exception as e:
    st.error(f"⚠️ Could not load chart data: {e}")
