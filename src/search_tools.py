from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup

class ResearchEngine:
    def __init__(self):
        self.ddg = DuckDuckGoSearchRun()

    def search_web(self, query):
        """
        Searches the web and returns a summary of results.
        Forces '2025' context to get the latest data.
        """
        # We enforce "late 2024/2025" to ensure fresh data for your report
        enhanced_query = f"{query} data figures trends December 2025 India Global"
        print(f"🌍 Searching: {enhanced_query}")
        
        try:
            results = self.ddg.run(enhanced_query)
            return results
        except Exception as e:
            return f"Search Error: {str(e)}"

    def scrape_url(self, url):
        """Deep scrapes a specific URL for full context"""
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            return docs[0].page_content[:5000] # Limit tokens
        except Exception as e:
            return f"Error scraping {url}: {e}"

    def deep_scrape(self, url):
        """
        If a specific URL is found, we scrape it for more context.
        """
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            content = docs[0].page_content
            # Clean up excessive whitespace
            clean_content = " ".join(content.split())
            return clean_content[:4000] # Limit to avoid token overflow
        except Exception as e:
            return f"Scraping Error for {url}: {e}"

    def get_market_data(self):
        """Simulate fetching specific indexes (Since no paid API)"""
        # In real prod, this would hit your scraped SIAM/FADA sources
        return "Market Context: EV Sales India Nov 2025: 140,000 units. Growth: 12% YoY."
