from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import News, Category, SavedArticle
from .forms import UserRegistrationForm
import feedparser
import requests
from django.conf import settings
from datetime import datetime
from dateutil import parser as date_parser
import re
import pytz
import time


# Country list for filtering
COUNTRIES = {
    'all': 'All Countries',
    'us': 'United States',
    'gb': 'United Kingdom',
    'in': 'India',
    'ca': 'Canada',
    'au': 'Australia',
    'de': 'Germany',
    'fr': 'France',
    'it': 'Italy',
    'es': 'Spain',
    'jp': 'Japan',
    'cn': 'China',
    'ru': 'Russia',
    'br': 'Brazil',
    'mx': 'Mexico',
    'za': 'South Africa',
    'ng': 'Nigeria',
    'eg': 'Egypt',
    'ae': 'UAE',
    'sa': 'Saudi Arabia',
    'kr': 'South Korea',
    'sg': 'Singapore',
    'my': 'Malaysia',
    'id': 'Indonesia',
    'ph': 'Philippines',
    'th': 'Thailand',
    'vn': 'Vietnam',
    'nz': 'New Zealand',
    'ie': 'Ireland',
    'nl': 'Netherlands',
    'be': 'Belgium',
    'ch': 'Switzerland',
    'at': 'Austria',
    'se': 'Sweden',
    'no': 'Norway',
    'dk': 'Denmark',
    'fi': 'Finland',
    'pl': 'Poland',
    'tr': 'Turkey',
    'ar': 'Argentina',
    'cl': 'Chile',
    'co': 'Colombia',
    'pe': 'Peru',
}


def home(request):
    """Home page with all news articles"""
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    country_code = request.GET.get('country', 'all')
    
    news_list = News.objects.all()
    
    # Filter by category
    if category_id:
        news_list = news_list.filter(category_id=category_id)
    
    # Filter by country
    if country_code and country_code != 'all':
        news_list = news_list.filter(country=country_code)
    
    # Search functionality
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(news_list, 12)  # 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories with counts
    categories = Category.objects.annotate(
        article_count=Count('news')
    ).order_by('name')
    
    # Get country counts
    country_counts = {}
    for code in COUNTRIES.keys():
        if code == 'all':
            country_counts[code] = News.objects.count()
        else:
            country_counts[code] = News.objects.filter(country=code).count()
    
    # Check which articles are saved by the user
    saved_article_ids = []
    if request.user.is_authenticated:
        saved_article_ids = SavedArticle.objects.filter(
            user=request.user
        ).values_list('news_id', flat=True)
    
    # Safely convert category_id to int
    selected_category = None
    if category_id:
        try:
            selected_category = int(category_id)
        except (ValueError, TypeError):
            selected_category = None
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'saved_article_ids': list(saved_article_ids),
        'countries': COUNTRIES,
        'country_counts': country_counts,
        'selected_country': country_code,
    }
    
    return render(request, 'newsapp/home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'newsapp/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'home')
            # Validate next_url to prevent open redirect vulnerability
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'newsapp/login.html')


@login_required
def dashboard(request):
    """User dashboard with saved articles"""
    saved_articles = SavedArticle.objects.filter(user=request.user).select_related('news')
    
    # Pagination
    paginator = Paginator(saved_articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'newsapp/dashboard.html', context)


@login_required
@require_POST
def save_article(request, news_id):
    """Save an article for later"""
    news = get_object_or_404(News, id=news_id)
    saved_article, created = SavedArticle.objects.get_or_create(
        user=request.user,
        news=news
    )
    
    if created:
        return JsonResponse({'status': 'saved', 'message': 'Article saved successfully!'})
    else:
        return JsonResponse({'status': 'already_saved', 'message': 'Article already saved!'})


@login_required
@require_POST
def unsave_article(request, news_id):
    """Remove an article from saved list"""
    news = get_object_or_404(News, id=news_id)
    SavedArticle.objects.filter(user=request.user, news=news).delete()
    
    return JsonResponse({'status': 'unsaved', 'message': 'Article removed from saved list!'})


def fetch_rss_feeds():
    """Fetch news from RSS feeds"""
    rss_feeds = [
        {
            'url': 'http://feeds.bbci.co.uk/news/rss.xml',
            'source': 'BBC',
            'category': 'World'
        },
        {
            'url': 'https://techcrunch.com/feed/',
            'source': 'TechCrunch',
            'category': 'Technology'
        },
        {
            'url': 'http://rss.cnn.com/rss/edition.rss',
            'source': 'CNN',
            'category': 'World'
        },
        {
            'url': 'https://www.espn.com/espn/rss/news',
            'source': 'ESPN',
            'category': 'Sports'
        },
        {
            'url': 'https://www.theguardian.com/world/rss',
            'source': 'Guardian',
            'category': 'World'
        },
    ]
    
    articles_added = 0
    
    for feed_config in rss_feeds:
        try:
            feed = feedparser.parse(feed_config['url'])
            
            if feed.bozo:
                print(f"Error parsing feed {feed_config['url']}: {feed.bozo_exception}")
                continue
            
            category, _ = Category.objects.get_or_create(
                name=feed_config['category'],
                defaults={'slug': feed_config['category'].lower().replace(' ', '-')}
            )
            
            for entry in feed.entries[:20]:  # Limit to 20 articles per feed
                try:
                    # Parse published date
                    published_date = timezone.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            # Ensure we have at least 6 elements
                            parsed = entry.published_parsed
                            if len(parsed) >= 6:
                                # Create timezone-aware datetime
                                published_date = datetime(*parsed[:6], tzinfo=pytz.UTC)
                                # Convert to Django's timezone-aware format
                                published_date = timezone.make_aware(
                                    published_date.replace(tzinfo=None), 
                                    pytz.UTC
                                )
                            else:
                                # Fill missing elements with defaults
                                parsed_list = list(parsed) + [0] * (6 - len(parsed))
                                published_date = datetime(*parsed_list[:6], tzinfo=pytz.UTC)
                                published_date = timezone.make_aware(
                                    published_date.replace(tzinfo=None), 
                                    pytz.UTC
                                )
                        except (ValueError, TypeError, IndexError):
                            published_date = timezone.now()
                    
                    # Extract image URL
                    image_url = ''
                    if hasattr(entry, 'media_content') and entry.media_content:
                        image_url = entry.media_content[0].get('url', '')
                    elif hasattr(entry, 'image'):
                        image_url = entry.image.get('href', '')
                    elif hasattr(entry, 'links'):
                        for link in entry.links:
                            if link.get('type', '').startswith('image'):
                                image_url = link.get('href', '')
                                break
                    
                    # Get description
                    description = ''
                    if hasattr(entry, 'description'):
                        description = entry.description or ''
                    elif hasattr(entry, 'summary'):
                        description = entry.summary or ''
                    
                    # Clean HTML from description
                    if description:
                        description = re.sub('<[^<]+?>', '', description)
                        description = description[:500]  # Limit length
                    
                    # Validate title and link
                    if not hasattr(entry, 'title') or not entry.title:
                        continue
                    if not hasattr(entry, 'link') or not entry.link:
                        continue
                    
                    # Create or update news article
                    news, created = News.objects.get_or_create(
                        link=entry.link,
                        defaults={
                            'title': (entry.title or 'Untitled')[:500],
                            'description': description,
                            'published_date': published_date,
                            'image_url': image_url,
                            'source': feed_config['source'],
                            'category': category,
                        }
                    )
                    
                    if created:
                        articles_added += 1
                        
                except Exception as e:
                    print(f"Error processing entry: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching feed {feed_config['url']}: {e}")
            continue
    
    return articles_added


def fetch_newsapi():
    """Fetch news from NewsData.io API with country support"""
    api_key = settings.NEWSAPI_KEY
    categories = ['technology', 'sports', 'business', 'entertainment', 'health', 'science']
    # Popular countries to fetch news from
    countries = ['us', 'gb', 'in', 'ca', 'au', 'de', 'fr', 'jp', 'cn', 'br']
    articles_added = 0
    
    for cat in categories:
        # Fetch from multiple countries
        for country_code in countries:
            try:
                # Add delay to avoid rate limiting (1 second between requests)
                time.sleep(1)
                
                # NewsData.io API endpoint
                url = 'https://newsdata.io/api/1/news'
                params = {
                    'apikey': api_key,
                    'category': cat,
                    'country': country_code,
                    'language': 'en'
                }
                
                # Add headers for better compatibility
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 'success':
                        # Get or create category
                        category_name = cat.capitalize()
                        category, _ = Category.objects.get_or_create(
                            name=category_name,
                            defaults={'slug': cat}
                        )
                        
                        for article in data.get('results', []):
                            try:
                                if not article.get('link'):
                                    continue
                                
                                # Parse published date
                                published_date = timezone.now()
                                if article.get('pubDate'):
                                    try:
                                        # NewsData.io uses ISO format or other formats
                                        pub_date_str = article['pubDate']
                                        # Try parsing different date formats
                                        try:
                                            published_date = datetime.fromisoformat(
                                                pub_date_str.replace('Z', '+00:00')
                                            )
                                        except:
                                            # Try parsing other common formats
                                            published_date = date_parser.parse(pub_date_str)
                                            # Ensure timezone-aware datetime
                                            if published_date.tzinfo is None:
                                                published_date = pytz.UTC.localize(published_date)
                                            # Convert to Django's timezone-aware datetime if needed
                                            # Note: pytz.UTC.localize already makes it timezone-aware
                                            # So this check should rarely be needed, but kept for safety
                                            if not timezone.is_aware(published_date):
                                                published_date = timezone.make_aware(
                                                    published_date.replace(tzinfo=None), 
                                                    pytz.UTC
                                                )
                                    except Exception as e:
                                        print(f"Date parsing error: {e}")
                                        published_date = timezone.now()
                                
                                # Get source name
                                source_name = article.get('source_id', 'NewsData.io')
                                if article.get('source_name'):
                                    source_name = article['source_name']
                                
                                # Get image URL
                                image_url = article.get('image_url', '') or article.get('image', '')
                                
                                # Get description
                                description = article.get('description', '') or article.get('content', '')
                                if description:
                                    # Clean HTML if present
                                    description = re.sub('<[^<]+?>', '', description)
                                    description = description[:500]  # Limit length
                                
                                # Validate required fields
                                title = article.get('title', '').strip()
                                if not title:
                                    title = 'Untitled'
                                
                                link = article.get('link', '').strip()
                                if not link:
                                    continue
                                
                                # Create or update news article
                                news, created = News.objects.get_or_create(
                                    link=link,
                                    defaults={
                                        'title': title[:500],
                                        'description': description,
                                        'published_date': published_date,
                                        'image_url': image_url,
                                        'source': source_name,
                                        'category': category,
                                        'country': country_code,
                                    }
                                )
                                
                                if created:
                                    articles_added += 1
                                    
                            except Exception as e:
                                print(f"Error processing NewsData.io article: {e}")
                                continue
                    else:
                        print(f"NewsData.io API returned error: {data.get('message', 'Unknown error')}")
                else:
                    error_text = response.text[:200] if response.text else 'No error message'
                    # Handle rate limiting with longer delay
                    if response.status_code == 429:
                        print(f"Rate limit hit for {cat}/{country_code}. Waiting 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"NewsData.io error: {response.status_code} - {error_text}")
                        
            except Exception as e:
                print(f"Error fetching NewsData.io category {cat} for country {country_code}: {e}")
                # Add delay even on error to avoid rapid retries
                time.sleep(1)
                continue
    
    return articles_added
