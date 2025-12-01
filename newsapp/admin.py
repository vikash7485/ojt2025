from django.contrib import admin
from .models import News, Category, SavedArticle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'category', 'country', 'published_date', 'created_at']
    list_filter = ['category', 'source', 'country', 'published_date']
    search_fields = ['title', 'description', 'source']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'


@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'news__title']
    date_hierarchy = 'saved_at'
