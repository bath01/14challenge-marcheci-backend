import logging
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from scraper.scrapers import SCRAPERS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape products from all registered sources and upsert into the database.'

    def handle(self, *args, **options):
        total_created = 0
        total_updated = 0

        for ScraperClass in SCRAPERS:
            scraper = ScraperClass()
            self.stdout.write(f'Running scraper: {scraper.source_name}')

            try:
                products = scraper.scrape()
            except Exception as e:
                self.stderr.write(f'Scraper {scraper.source_name} failed: {e}')
                logger.exception('Scraper %s failed', scraper.source_name)
                continue

            for data in products:
                created, updated = self._upsert_product(data, scraper.source_name)
                total_created += created
                total_updated += updated

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Created: {total_created}, Updated: {total_updated}'
            )
        )

    def _upsert_product(self, data: dict, source: str) -> tuple[int, int]:
        category = None
        category_name = data.pop('category_name', None)
        if category_name:
            slug = slugify(category_name)
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': category_name},
            )

        product_url = data.get('product_url', '')
        if not product_url:
            return 0, 0

        product, created = Product.objects.update_or_create(
            product_url=product_url,
            defaults={
                **data,
                'category': category,
                'source': source,
            },
        )

        return (1, 0) if created else (0, 1)
