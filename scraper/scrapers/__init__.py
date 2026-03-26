from scraper.scrapers.phones_scraper import PhonesScraper

from .books_scraper import BooksScraper

# Register all scrapers here — they will all be run by the management command
SCRAPERS = [
    PhonesScraper,
    BooksScraper,
]
