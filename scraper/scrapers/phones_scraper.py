"""
Example scraper targeting books.toscrape.com — a legal practice scraping site.
Replace or extend this with your own target scraper.
"""
import logging
from bs4 import BeautifulSoup
from .base import BaseScraper

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.jumia.ci'
RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


class PhonesScraper(BaseScraper):
    source_name = 'jumia.ci'

    def scrape(self) -> list[dict]:
        products = []
        url = f'{BASE_URL}/telephone-tablette'

        while url:
            logger.info('Scraping page: %s', url)
            try:
                response = self.get(url)
            except Exception:
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            for article in soup.select('article.prd'):
                products.append(self._parse_article(article))

            next_btn = soup.select_one('li.next > a')
            if next_btn:
                current_dir = url.rsplit('/', 1)[0]
                url = f'{current_dir}/{next_btn["href"]}'
            else:
                url = None

        logger.info('Scraped %d products from %s', len(products), self.source_name)
        return products

    def _parse_article(self, article) -> dict:
        title_tag = article.select_one('div.info > h3')
        title = title_tag['title'] if title_tag else ''
        relative_url = article.select_one('div.info > a')['href']
        product_url = f'{BASE_URL}/{relative_url}'

        price_text = article.select_one('.price_color')
        price = None
        if price_text:
            raw = price_text.text.strip().replace('Â', '').replace('£', '').strip()
            try:
                price = float(raw)
            except ValueError:
                pass

        rating_class = article.select_one('p.star-rating')
        rating_word = rating_class['class'][1] if rating_class else None
        rating = RATING_MAP.get(rating_word)

        img_tag = article.select_one('img')
        image_url = ''
        if img_tag:
            src = img_tag.get('src', '')
            image_url = f"{BASE_URL}/{src.replace('../', '')}"

        return {
            'title': title,
            'description': '',
            'price': price,
            'currency': 'GBP',
            'image_url': image_url,
            'product_url': product_url,
            'category_name': 'Books',
            'rating': rating,
            'in_stock': True,
        }
