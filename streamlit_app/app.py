import streamlit as st
import requests
import json
import yfinance as yf

st.set_page_config(page_title="🧠💬 AI Finance Assistant", layout="wide")
st.title("🧠💬 AI Finance Assistant")
st.write("Ask anything about a company's stock and get insights with voice support.")

# Country selector
country = st.selectbox("Select Country", ["United States", "India"])

# Stock symbols
stock_options = {
    "United States": {
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "Google (GOOGL)": "GOOGL",
        "Microsoft (MSFT)": "MSFT",
        "Amazon (AMZN)": "AMZN"
    },
    "India": {
        "Reliance Industries (RELIANCE.NS)": "RELIANCE.NS",
        "Tata Consultancy Services (TCS.NS)": "TCS.NS",
        "Infosys (INFY.NS)": "INFY.NS",
        "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS",
        "ICICI Bank (ICICIBANK.NS)": "ICICIBANK.NS"
    }
}

stock_name = st.selectbox("Select Stock", list(stock_options[country].keys()))
stock_symbol = stock_options[country][stock_name]

query = st.text_input("Enter your financial question", "What is the current stock price?")

if st.button("Ask"):
    with st.spinner("🤖 Thinking..."):
        try:
            url = "https://nani2906-my-fastapi-backend.hf.space/ask"  # Your deployed backend URL
            payload = json.dumps({
                "query": query,
                "stock_symbol": stock_symbol
            })
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, data=payload, headers=headers, timeout=90)

            if response.status_code == 200:
                result = response.json()

                st.subheader("📈 Stock Data")
                st.json(result.get("stock_data", {}))

                st.subheader("📰 Latest News")
                for news in result.get("news", []):
                    st.markdown(f"- {news}")

                st.subheader("📄 Relevant Documents")
                for doc in result.get("documents", []):
                    st.markdown(f"- {doc}")

                st.subheader("🧠 Summary")
                summary = result.get("summary", "No summary available.")
                st.success(summary)

                audio_data = result.get("audio")
                if audio_data:
                    st.subheader("🔊 Voice Summary")
                    st.audio(audio_data.encode("ISO-8859-1"), format="audio/mp3")
                else:
                    st.warning("⚠️ Audio not available.")

            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Request failed: {e}")

# Charts
st.markdown("---")
st.subheader("📊 Stock Price Chart (Last 30 Days)")
try:
    df = yf.Ticker(stock_symbol).history(period="30d")
    if not df.empty:
        st.line_chart(df['Close'], use_container_width=True)
        st.bar_chart(df['Volume'], use_container_width=True)
    else:
        st.warning("📉 No chart data available.")
except Exception as e:
    st.error(f"⚠️ Error loading chart: {e}")
