from django.contrib import admin
from .models import Board, Category, Feed


class BoardAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'public', 'updated_at', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'total_feed_count', 'updated_at', 'created_at')


class FeedAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'image_url', 'feed_url', 'category', 'updated_at', 'created_at')


admin.site.register(Board, BoardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)