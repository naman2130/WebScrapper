class ScraperCache:
    """A simple in-memory cache for storing product details."""

    def __init__(self):
        self.cache = {}

    def is_changed(self, title: str, price: float) -> bool:
        """Check if the product price has changed."""
        if title not in self.cache or self.cache[title] != price:
            self.cache[title] = price
            return True
        return False
