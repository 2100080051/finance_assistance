

import requests
from bs4 import BeautifulSoup

class ScrapingAgent:
    def __init__(self):
        self.base_url = "https://finance.yahoo.com"

    def get_news_headlines(self, count=5):
        """
        Scrape latest news headlines from Yahoo Finance
        Returns:
            List of dictionaries with title and URL
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(self.base_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = soup.find_all("a", href=True)
        news_items = []

        for tag in headlines:
            href = tag["href"]
            title = tag.get_text().strip()

         
            if "/news/" in href and title and len(title) > 20:
                link = f"https://finance.yahoo.com{href}" if href.startswith("/") else href
                news_items.append({"title": title, "url": link})

                if len(news_items) >= count:
                    break

        return news_items


if __name__ == "__main__":
    agent = ScrapingAgent()
    headlines = agent.get_news_headlines()
    for item in headlines:
        print(f"📰 {item['title']}\n🔗 {item['url']}\n")
