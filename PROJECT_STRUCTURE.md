# Project Structure

## Complete Folder Structure

```
g6/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Complete documentation
├── QUICKSTART.md                      # Quick start guide
├── PROJECT_STRUCTURE.md               # This file
├── setup.py                           # Setup script
├── .gitignore                         # Git ignore rules
│
├── newsaggregator/                    # Django project (settings)
│   ├── __init__.py
│   ├── settings.py                    # Project settings & configuration
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
│
├── newsapp/                           # Main application
│   ├── __init__.py
│   ├── admin.py                       # Admin interface configuration
│   ├── models.py                      # Database models (News, Category, SavedArticle)
│   ├── views.py                       # View functions (home, register, login, dashboard, etc.)
│   ├── urls.py                        # App URL routing
│   ├── forms.py                       # User registration form
│   ├── apps.py                        # App configuration
│   ├── tests.py                       # Test cases
│   │
│   ├── management/                    # Management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── fetch_news.py          # Command: python manage.py fetch_news
│   │
│   └── migrations/                    # Database migrations
│       └── __init__.py
│
├── templates/                         # HTML templates
│   ├── base.html                      # Base template with navigation
│   └── newsapp/
│       ├── home.html                  # Home page with news feed
│       ├── login.html                 # Login page
│       ├── register.html              # Registration page
│       └── dashboard.html             # User dashboard (saved articles)
│
└── static/                            # Static files (CSS, JS, images)
    ├── css/
    │   └── style.css                  # Custom styles
    └── js/
        └── main.js                    # JavaScript for AJAX functionality
```

## Key Files Description

### Models (newsapp/models.py)
- **Category**: News categories (Technology, Sports, Business, etc.)
- **News**: News articles from RSS feeds and NewsAPI
- **SavedArticle**: User's saved articles (many-to-many relationship)

### Views (newsapp/views.py)
- `home()`: Display all news with filtering and pagination
- `register()`: User registration
- `login_view()`: User login
- `dashboard()`: User's saved articles
- `save_article()`: AJAX endpoint to save article
- `unsave_article()`: AJAX endpoint to remove saved article
- `fetch_rss_feeds()`: Fetch from RSS feeds
- `fetch_newsapi()`: Fetch from NewsAPI

### URLs
- Main: `newsaggregator/urls.py` - Routes to app URLs
- App: `newsapp/urls.py` - App-specific routes

### Management Command
- `fetch_news`: Fetches news from RSS feeds and NewsAPI
  - Usage: `python manage.py fetch_news`
  - Options: `--rss-only`, `--newsapi-only`

### Templates
- Bootstrap 5 based responsive design
- AJAX-powered save/unsave functionality
- Category filtering sidebar
- Search functionality
- Pagination

### Static Files
- **style.css**: Custom styling and animations
- **main.js**: AJAX handlers for save/unsave, toast notifications

## Database Schema

### News Table
- id (Primary Key)
- title (CharField, max 500)
- description (TextField)
- link (URLField, unique)
- published_date (DateTimeField)
- image_url (URLField)
- source (CharField)
- category_id (ForeignKey to Category)
- created_at, updated_at (timestamps)

### Category Table
- id (Primary Key)
- name (CharField, unique)
- slug (SlugField, unique)
- description (TextField)
- created_at (timestamp)

### SavedArticle Table
- id (Primary Key)
- user_id (ForeignKey to User)
- news_id (ForeignKey to News)
- saved_at (timestamp)
- Unique constraint on (user_id, news_id)

## API Integration

### RSS Feeds
- BBC News
- TechCrunch
- CNN
- ESPN
- Guardian

### NewsAPI
- Categories: Technology, Sports, Business, Entertainment, Health
- API Key configured in settings.py

## Features Implemented

✅ Multi-source news aggregation
✅ Category filtering
✅ Save for later / bookmarking
✅ User authentication (register, login, logout)
✅ Responsive Bootstrap UI
✅ Pagination
✅ Search functionality
✅ Management command for RSS fetching
✅ AJAX-based save/unsave
✅ Dashboard for saved articles

