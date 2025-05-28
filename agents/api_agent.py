# data_ingestion/api_agent.py

import yfinance as yf

class APIAgent:
    def __init__(self):
        pass

    def get_stock_data(self, symbol: str, period: str = "1d", interval: str = "1h"):
        """
        Fetch stock data using Yahoo Finance
        Args:
            symbol: e.g., "TSLA", "AAPL"
            period: e.g., "1d", "5d", "1mo"
            interval: e.g., "1m", "5m", "1h", "1d"
        Returns:
            Dictionary with latest stock info
        """
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        info = stock.info

        return {
            "symbol": symbol,
            "price": hist['Close'].iloc[-1] if not hist.empty else "N/A",
            "previous_close": info.get("previousClose", "N/A"),
            "open": info.get("open", "N/A"),
            "volume": info.get("volume", "N/A"),
            "currency": info.get("currency", "USD")
        }

# Test it directly
if __name__ == "__main__":
    agent = APIAgent()
    data = agent.get_stock_data("AAPL")
    print(data)
