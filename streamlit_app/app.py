import streamlit as st
import requests
import json
import yfinance as yf

st.set_page_config(page_title="🧠💬 AI Finance Assistant", layout="wide")
st.title("🧠💬 AI Finance Assistant")
st.write("Ask anything about a company's stock and get insights with voice support.")

# Step 1: Country selector
country = st.selectbox("Select Country", ["United States", "India"], index=0)

# Step 2: Define stock options based on country
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

# Step 3: Stock dropdown based on selected country
stock_name = st.selectbox("Select Stock", list(stock_options[country].keys()))
stock_symbol = stock_options[country][stock_name]

# Step 4: User query
query = st.text_input("Enter your financial question", "What is the current stock price?")

# Step 5: Send request to FastAPI
if st.button("Ask"):
    with st.spinner("Thinking... 🤖"):
        try:
            url = "https://nani2906-my-fastapi-backend.hf.space/ask"  # Backend URL
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"query": query, "stock_symbol": stock_symbol})

            response = requests.post(url, headers=headers, data=payload, timeout=90)

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
                summary = result.get("summary", "No summary available.")
                st.success(summary)

                # 🔊 Voice output via JavaScript in the browser
                st.markdown(f"""
                <script>
                var msg = new SpeechSynthesisUtterance({json.dumps(summary)});
                window.speechSynthesis.speak(msg);
                </script>
                """, unsafe_allow_html=True)

            else:
                st.error(f"❌ API returned status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Something went wrong: {e}")

# Step 6: Optional Charts
st.markdown("---")
st.subheader("📊 Stock Price Chart (Last 30 Days)")
try:
    df = yf.Ticker(stock_symbol).history(period="30d")
    if not df.empty:
        st.line_chart(df['Close'], use_container_width=True)
        st.bar_chart(df['Volume'], use_container_width=True)
    else:
        st.warning("No historical data available for this stock.")
except Exception as e:
    st.error(f"⚠️ Could not load chart data: {e}")
