# News Aggregator Web Application

A comprehensive Django-based news aggregation platform that collects news from multiple RSS feeds and NewsAPI, allowing users to browse, filter, save, and manage their favorite articles.

## 🚀 Features

### Core Features
- **Multi-Source News Aggregation**: Fetches news from RSS feeds (BBC, TechCrunch, CNN, ESPN, Guardian) and NewsAPI
- **Category Filtering**: Filter articles by categories (Technology, Sports, Business, Entertainment, Health, World)
- **Save for Later**: Bookmark articles to read later with a personalized dashboard
- **User Authentication**: Complete registration, login, and logout system
- **Responsive UI**: Modern Bootstrap 5 interface with mobile-friendly design
- **Pagination**: Efficient pagination for large article lists
- **Search Functionality**: Search articles by title and description

### Technical Features
- RSS feed parsing using `feedparser`
- NewsAPI integration
- Duplicate article detection
- Scheduled news fetching via management command
- AJAX-based save/unsave functionality
- Category-based filtering with article counts

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation

### 1. Clone or Navigate to Project Directory

```bash
cd g6
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional - for Admin Access)

```bash
python manage.py createsuperuser
```

### 6. Fetch Initial News Data

```bash
python manage.py fetch_news
```

This command will:
- Fetch articles from RSS feeds (BBC, TechCrunch, CNN, ESPN, Guardian)
- Fetch articles from NewsAPI (Technology, Sports, Business, Entertainment, Health)
- Create categories automatically
- Store articles in the database

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
g6/
├── newsaggregator/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── newsapp/                 # Main application
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL routing
│   ├── forms.py            # User registration form
│   ├── management/
│   │   └── commands/
│   │       └── fetch_news.py  # Management command
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── newsapp/
│       ├── home.html       # Home page
│       ├── login.html     # Login page
│       ├── register.html  # Registration page
│       └── dashboard.html # User dashboard
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js        # JavaScript functionality
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🗄️ Database Models

### News
- `title`: Article title
- `description`: Article description/summary
- `link`: Original article URL
- `published_date`: Publication date
- `image_url`: Article image URL
- `source`: News source name
- `category`: Foreign key to Category
- `created_at`: Record creation timestamp
- `updated_at`: Record update timestamp

### Category
- `name`: Category name (e.g., "Technology", "Sports")
- `slug`: URL-friendly slug
- `description`: Category description
- `created_at`: Record creation timestamp

### SavedArticle
- `user`: Foreign key to User
- `news`: Foreign key to News
- `saved_at`: Timestamp when article was saved

## 🔧 Management Commands

### Fetch News

Fetch news from RSS feeds and NewsAPI:

```bash
python manage.py fetch_news
```

**Options:**
- `--rss-only`: Fetch only from RSS feeds
- `--newsapi-only`: Fetch only from NewsAPI

**Example:**
```bash
python manage.py fetch_news --rss-only
```

## 🔐 User Authentication

### Registration
- Navigate to `/register/`
- Fill in username, email, password, and optional first/last name
- Account is created and you can log in

### Login
- Navigate to `/login/`
- Enter username and password
- Redirects to home page after successful login

### Logout
- Click on your username in the navbar
- Select "Logout"

## 📱 Usage Guide

### Browsing News
1. Visit the home page to see all aggregated news
2. Use the category sidebar to filter by category
3. Use the search bar to search for specific articles
4. Click "Read More" to open the original article

### Saving Articles
1. Log in to your account
2. Click the bookmark icon on any article card
3. Saved articles appear in your dashboard
4. Access saved articles from "My Dashboard" in the navbar

### Dashboard
1. Click "My Dashboard" in the navbar
2. View all your saved articles
3. Remove articles by clicking "Remove" button
4. Click "Read More" to open articles

## 🔄 Scheduled News Fetching

To set up automatic news fetching, you can use:

### Option 1: Cron Job (Linux/Mac)
```bash
# Add to crontab (runs every hour)
0 * * * * cd /path/to/g6 && /path/to/venv/bin/python manage.py fetch_news
```

### Option 2: Windows Task Scheduler
1. Open Task Scheduler
2. Create a new task
3. Set trigger (e.g., daily at specific time)
4. Set action: `python manage.py fetch_news`
5. Set working directory to project folder

### Option 3: Django-APScheduler (Optional)
Install django-apscheduler and configure in settings.py for in-app scheduling.

## 🧪 Testing

### Manual Testing Checklist

1. **User Registration**
   - [ ] Register a new user
   - [ ] Verify email validation
   - [ ] Verify password requirements

2. **User Login/Logout**
   - [ ] Login with valid credentials
   - [ ] Login with invalid credentials
   - [ ] Logout functionality

3. **News Display**
   - [ ] Home page displays articles
   - [ ] Pagination works correctly
   - [ ] Images load properly (or show placeholder)

4. **Category Filtering**
   - [ ] Filter by each category
   - [ ] Category counts are accurate
   - [ ] "All News" shows all articles

5. **Search Functionality**
   - [ ] Search by title
   - [ ] Search by description
   - [ ] Clear search works

6. **Save/Unsave Articles**
   - [ ] Save article when logged in
   - [ ] Unsave article
   - [ ] Saved articles appear in dashboard
   - [ ] Remove articles from dashboard

7. **Management Command**
   - [ ] `fetch_news` command runs successfully
   - [ ] Articles are added to database
   - [ ] Duplicates are not created

## 🐛 Troubleshooting

### Issue: No articles showing
**Solution:** Run the management command to fetch news:
```bash
python manage.py fetch_news
```

### Issue: Static files not loading
**Solution:** 
1. Ensure `STATICFILES_DIRS` is set in settings.py
2. Run `python manage.py collectstatic` (for production)
3. Check that static files are in the `static/` directory

### Issue: NewsAPI errors
**Solution:**
1. Verify API key in settings.py
2. Check internet connection
3. Verify API key is valid and has remaining requests

### Issue: RSS feed errors
**Solution:**
1. Check internet connection
2. Verify RSS feed URLs are accessible
3. Some feeds may be temporarily unavailable

## 🔑 API Configuration

The NewsAPI key is configured in `newsaggregator/settings.py`:

```python
NEWSAPI_KEY = 'pub_71ac1cf53f2746feb2266421d769c929'
```

## 📝 RSS Feed Sources

The application fetches from the following RSS feeds:
- BBC News: `http://feeds.bbci.co.uk/news/rss.xml`
- TechCrunch: `https://techcrunch.com/feed/`
- CNN: `http://rss.cnn.com/rss/edition.rss`
- ESPN: `https://www.espn.com/espn/rss/news`
- Guardian: `https://www.theguardian.com/world/rss`

## 🚀 Deployment

### Production Checklist

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use PostgreSQL instead of SQLite
4. Set up proper static file serving
5. Configure environment variables for sensitive data
6. Set up HTTPS
7. Configure proper database backups

### Environment Variables (Recommended)

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

## 📄 License

This project is open source and available for educational purposes.

## 👥 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check RSS feed accessibility
4. Verify API key validity

## 🎯 Future Enhancements

Potential features for future development:
- Search system with advanced filters
- User preferences and customization
- Dark mode toggle
- Sentiment analysis badges
- Trending articles section
- Email digest functionality
- Social sharing buttons
- Date range filters
- PDF export functionality
- Real-time notifications

---

**Built with Django, Bootstrap, and ❤️**

