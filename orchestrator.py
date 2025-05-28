from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from agents.api_agent import APIFinanceAgent
from agents.scraping_agent import ScrapingAgent
from agents.retriever_agent import RetrieverAgent
from agents.language_agent import LanguageAgent
from agents.voice_agent import VoiceAgent

app = FastAPI(
    title="🧠💬 AI Finance Assistant",
    description="Ask anything about a company's stock and get insights with voice support.",
    version="0.1.0"
)

# Initialize agents
api_agent = APIFinanceAgent()
scraping_agent = ScrapingAgent()
retriever_agent = RetrieverAgent()
language_agent = LanguageAgent()
voice_agent = VoiceAgent()

# Request body model
class QueryInput(BaseModel):
    query: str
    stock_symbol: str = "AAPL"

@app.get("/")
def root():
    return {
        "message": "✅ Finance Assistant API is running!",
        "docs_url": "http://127.0.0.1:8000/docs",
        "how_to_use": "Send a POST request to /ask with 'query' and 'stock_symbol'."
    }

@app.post("/ask")
def ask_finance_assistant(data: QueryInput, background_tasks: BackgroundTasks):
    query = data.query
    symbol = data.stock_symbol

    # 1. Get API data
    stock_data = api_agent.get_stock_price(symbol)

    # 2. Scrape recent news
    news_data = scraping_agent.get_news_headlines(count=3)

    # 3. Retrieve documents (e.g., financial reports)
    retrieved_docs = retriever_agent.query(query)

    # 4. Generate summary
    final_summary = language_agent.generate_summary(stock_data, news_data, retrieved_docs)

    # 5. Speak in background to avoid timeout
    background_tasks.add_task(voice_agent.speak_text, final_summary)

    # 6. Return response immediately
    return {
        "query": query,
        "stock_data": stock_data,
        "news": news_data,
        "documents": retrieved_docs,
        "summary": final_summary
    }
