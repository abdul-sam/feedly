from django.contrib import admin
from .models import Article, Board, Category, Feed


class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'image_url', 'link', 'read', 'read_later', 'recently_read', 'feed', 'board', 'updated_at', 'created_at')


class BoardAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'public', 'updated_at', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'total_feed_count', 'updated_at', 'created_at')


class FeedAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'image_url', 'feed_url', 'category', 'article_count', 'updated_at', 'created_at')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)