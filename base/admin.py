from django.contrib import admin
from .models import Category, Feed

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'total_feed_count', 'updated_at', 'created_at')


class FeedAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'image_url', 'feed_url', 'category', 'updated_at', 'created_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)