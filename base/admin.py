from django.contrib import admin
from .models import Article, Board, Category, Favorite, Feed, Reading


class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'image_url', 'link', 'feed_title', 'updated_at', 'created_at')


class BoardAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'public', 'user', 'updated_at', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'total_feed_count', 'user', 'updated_at', 'created_at')


class FeedAdmin(admin.ModelAdmin):
  fields = ["feed_url"]

  list_display = ('title', 'description', 'image_url', 'feed_url', 'article_count', 'updated_at', 'created_at')
  

class FavoriteAdmin(admin.ModelAdmin):
  list_display = ('favorite', 'favorite_type', 'feed', 'user', 'updated_at', 'created_at')


class ReadingAdmin(admin.ModelAdmin):
  list_display = ('read_later', 'recently_read', 'article', 'user', 'updated_at', 'created_at')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Reading, ReadingAdmin)