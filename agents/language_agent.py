

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LanguageAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")  # Required for Groq
        )

    def generate_summary(self, stock_data, news_data, doc_chunks):
        news_text = "\n".join([f"- {item['title']}" for item in news_data])
        doc_text = "\n".join(doc_chunks)

        prompt = f"""
        You're a finance assistant. Give a short spoken-style market briefing based on:

        📊 Stock Info:
        {stock_data}

        📰 News Headlines:
        {news_text}

        📄 Key Document Insights:
        {doc_text}

        Be brief, professional, and under 200 words.
        """

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",  # or "mixtral-8x7b-32768", etc.
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()


# Test
if __name__ == "__main__":
    dummy_stock = {"symbol": "AAPL", "price": 195.3, "open": 193.6}
    dummy_news = [{"title": "Apple hits all-time high"}, {"title": "Nvidia dominates AI market"}]
    dummy_docs = ["Apple's revenue reached $394B", "Strong iPhone growth seen"]

    agent = LanguageAgent()
    print(agent.generate_summary(dummy_stock, dummy_news, dummy_docs))
