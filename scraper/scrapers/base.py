import logging
import requests
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


class BaseScraper(ABC):
    """Base class for all scrapers."""

    source_name: str = ''

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def get(self, url: str) -> requests.Response:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error('Request failed for %s: %s', url, e)
            raise

    @abstractmethod
    def scrape(self) -> list[dict]:
        """
        Run the scraping logic.
        Returns a list of product dicts with keys:
          title, description, price, currency, image_url,
          product_url, category_name, rating, in_stock
        """
        ...
