# agents/api_agent.py

import yfinance as yf

class APIFinanceAgent:
    def get_stock_price(self, symbol="AAPL"):
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            return {"error": f"No data found for symbol: {symbol}"}
        latest = data.iloc[-1]
        return {
            "symbol": symbol,
            "price": float(latest["Close"]),
            "previous_close": float(latest["Close"]),
            "open": float(latest["Open"]),
            "volume": int(latest["Volume"]),
            "currency": "USD"
        }


# Test it directly
if __name__ == "__main__":
    agent = APIFinanceAgent()
    data = agent.get_stock_data("AAPL")
    print(data)
