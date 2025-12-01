from django.core.management.base import BaseCommand
from newsapp.views import fetch_rss_feeds, fetch_newsapi


class Command(BaseCommand):
    help = 'Fetch news articles from RSS feeds and NewsAPI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rss-only',
            action='store_true',
            help='Fetch only from RSS feeds',
        )
        parser.add_argument(
            '--newsapi-only',
            action='store_true',
            help='Fetch only from NewsAPI',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting news fetch...'))
        
        rss_count = 0
        newsapi_count = 0
        
        if not options['newsapi_only']:
            self.stdout.write('Fetching from RSS feeds...')
            rss_count = fetch_rss_feeds()
            self.stdout.write(self.style.SUCCESS(f'Added {rss_count} articles from RSS feeds'))
        
        if not options['rss_only']:
            self.stdout.write('Fetching from NewsAPI...')
            newsapi_count = fetch_newsapi()
            self.stdout.write(self.style.SUCCESS(f'Added {newsapi_count} articles from NewsAPI'))
        
        total = rss_count + newsapi_count
        self.stdout.write(self.style.SUCCESS(f'\nTotal articles added: {total}'))

