from fastapi import FastAPI, Depends, Query, Header
from auth import authenticate
from scraper import ProductScraper
from storage import ScraperStorage
from cache import ScraperCache

app = FastAPI()

async def verify_token(authorization: str = Header(...)):
    authenticate(authorization)  # This will raise an HTTPException if the token is invalid

@app.post("/scrape")
async def scrape(
    limit_pages: int = Query(None, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string to use"),
    _: str = Depends(verify_token)  # Dependency to enforce authentication
):
    """Scrapes product data with optional page limit and proxy."""
    base_url = "https://dentalstall.com/shop"
    cache = ScraperCache()
    storage = ScraperStorage()

    scraper = ProductScraper(base_url=base_url, limit_pages=limit_pages, proxy=proxy, cache=cache, storage=storage)
    products_scraped = scraper.scrape()
    return {"status": "success", "products_scraped": len(products_scraped)}
