from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

class Category(models.Model):
  name = models.CharField(max_length=200, null=False)
  user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
  total_feed_count = models.IntegerField(default=0)
  favorit = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  

class Board(models.Model):
  title = models.CharField(max_length=200, null=False)
  description = models.TextField()
  user = models.ForeignKey(User, related_name='boards', on_delete=models.CASCADE)
  public = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Feed(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_url = models.CharField(max_length=2083)
  feed_url = models.CharField(max_length=2083)
  article_count = models.IntegerField(default=0)
  categories = models.ManyToManyField(Category)
  users = models.ManyToManyField(User)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def import_feed_link(self):
    return format_html('<a href="/feeds/{}/import-feed">Import Feed</a>', self.id)
  
  import_feed_link.short_description = "Import Feed"


class Favorite(models.Model):
  favorite = models.BooleanField(default=False)
  user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE, null=False)
  feed = models.ForeignKey(Feed, related_name='favorites', on_delete=models.CASCADE, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_url = models.CharField(max_length=2083)
  link = models.CharField(null=True)
  feed = models.ForeignKey(Feed, related_name='articles', on_delete=models.CASCADE)
  boards = models.ManyToManyField(Board)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Reading(models.Model):
  read_later = models.BooleanField(default=False)
  recently_read = models.BooleanField(default=False)
  user = models.ForeignKey(User, related_name='readings', on_delete=models.CASCADE, null=False)
  article = models.ForeignKey(Article, related_name='readings', on_delete=models.CASCADE, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)