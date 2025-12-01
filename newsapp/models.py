from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """News categories for filtering articles"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    """News articles from RSS feeds and NewsAPI"""
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=1000, unique=True)
    published_date = models.DateTimeField()
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    source = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=10, blank=True, null=True, db_index=True, help_text='ISO country code (e.g., us, gb, in)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title[:100]


class SavedArticle(models.Model):
    """Articles saved by users for later reading"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'news']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} - {self.news.title[:50]}"
