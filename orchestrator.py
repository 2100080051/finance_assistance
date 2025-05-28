from fastapi import FastAPI
from pydantic import BaseModel

from agents.api_agent import APIFinanceAgent
from agents.scraping_agent import ScrapingAgent
from agents.retriever_agent import RetrieverAgent
from agents.language_agent import LanguageAgent
from agents.voice_agent import VoiceAgent

app = FastAPI()

api_agent = APIFinanceAgent()
scraping_agent = ScrapingAgent()
retriever_agent = RetrieverAgent()
language_agent = LanguageAgent()
voice_agent = VoiceAgent()

class QueryInput(BaseModel):
    query: str
    stock_symbol: str = "AAPL"

@app.post("/ask")
def ask_finance_assistant(data: QueryInput):
    query = data.query
    symbol = data.stock_symbol

    stock_data = api_agent.get_stock_price(symbol)
    news_data = scraping_agent.get_news_headlines(count=3)
    retrieved_docs = retriever_agent.query(query)
    final_summary = language_agent.generate_summary(stock_data, news_data, retrieved_docs)

    voice_agent.speak_text(final_summary)

    return {
        "query": query,
        "stock_data": stock_data,
        "news": news_data,
        "documents": retrieved_docs,
        "summary": final_summary
    }
