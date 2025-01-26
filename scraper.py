import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from cache import ScraperCache
from storage import ScraperStorage

class ProductScraper:
    """Scrapes product data from a target website."""

    def __init__(self, base_url: str, limit_pages: int, proxy: str, cache: ScraperCache, storage: ScraperStorage):
        self.base_url = base_url
        self.limit_pages = limit_pages
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.cache = cache
        self.storage = storage

    def fetch_page(self, url: str) -> str:
        """Fetches the HTML content of a given URL."""
        try:
            response = requests.get(url, proxies=self.proxy, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def scrape_page(self, page_content: str) -> List[Dict]:
        """Scrapes product details from a single page."""
        soup = BeautifulSoup(page_content, "html.parser")
        products = []

        for product_div in soup.find_all("div", class_="product-inner"):
            title = product_div.find("h2", class_="woo-loop-product__title").text.strip()
            price_str = product_div.find("span", class_="woocommerce-Price-amount").text.strip()
            price = float(price_str.replace("₹", "").replace(",", ""))
            image_url = product_div.find("img", class_="attachment-woocommerce_thumbnail")["src"]
            image_path = self.storage.save_image(image_url)

            products.append({
                "product_title": title,
                "product_price": price,
                "path_to_image": image_path,
            })

        return products

    def scrape(self) -> List[Dict]:
        """Main scraping logic for the entire catalog."""
        products = []
        page = 1

        while not self.limit_pages or page <= self.limit_pages:
            url = f"{self.base_url}/page/{page}/"
            print(f"Scraping {url}...")

            html_content = self.fetch_page(url)
            if not html_content:
                print(f"Failed to fetch page {page}.")
                break

            scraped_products = self.scrape_page(html_content)

            for product in scraped_products:
                if not self.cache.is_changed(product["product_title"], product["product_price"]):
                    continue
                products.append(product)

            page += 1
            time.sleep(2)  # Avoid overloading the server

        self.storage.save_to_file(products)
        print(f"Scraping completed. Total products scraped: {len(products)}")
        return products