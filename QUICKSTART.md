# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Fetch News
```bash
python manage.py fetch_news
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Open Browser
Navigate to: `http://127.0.0.1:8000/`

## 📝 First Steps

1. **Register an Account**
   - Click "Register" in the navbar
   - Fill in your details
   - Login with your credentials

2. **Browse News**
   - View all articles on the home page
   - Filter by category using the sidebar
   - Search for specific topics

3. **Save Articles**
   - Click the bookmark icon on any article
   - View saved articles in "My Dashboard"

4. **Fetch More News**
   - Run `python manage.py fetch_news` periodically
   - Or set up a scheduled task (see README.md)

## 🔧 Troubleshooting

**No articles showing?**
```bash
python manage.py fetch_news
```

**Static files not loading?**
- Ensure `static/` folder exists with `css/` and `js/` subfolders
- Check `STATICFILES_DIRS` in settings.py

**Database errors?**
```bash
python manage.py migrate
```

## 📚 Full Documentation

See `README.md` for complete documentation.

