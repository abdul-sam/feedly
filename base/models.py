from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
  name = models.CharField(max_length=200, null=False)
  user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
  total_feed_count = models.IntegerField(default=0)
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


class Folder(models.Model):
  name = models.CharField(max_length=200, null=False)
  user = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
  total_article_count = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['-created_at']


class Feed(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_url = models.CharField(max_length=2083)
  feed_url = models.CharField(max_length=2083)
  article_count = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title


class FolderFeed(models.Model):
  folder = models.ForeignKey(Folder, related_name='folder_feeds', on_delete=models.CASCADE, null=False)
  feed = models.ForeignKey(Feed, related_name='folder_feeds', on_delete=models.CASCADE, null=False)
  user = models.ForeignKey(User, related_name='folder_feeds', on_delete=models.CASCADE, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



class Favorite(models.Model):
  favorite = models.BooleanField(default=False)
  favorite_type = models.CharField(null=False)
  user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE, null=False)
  feed = models.ForeignKey(Feed, related_name='favorites', on_delete=models.CASCADE, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_url = models.TextField()
  link = models.CharField(null=True)
  feed = models.ForeignKey(Feed, related_name='articles', on_delete=models.CASCADE)
  boards = models.ManyToManyField(Board)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def feed_title(self):
    return format_html('<a href="/admin/base/feeds/{}/change">{}</a>', self.id, self.feed.title)

  feed_title.short_description = "Feed"


class Reading(models.Model):
  read_later = models.BooleanField(default=False)
  recently_read = models.BooleanField(default=False)
  user = models.ForeignKey(User, related_name='readings', on_delete=models.CASCADE, null=False)
  article = models.ForeignKey(Article, related_name='readings', on_delete=models.CASCADE, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



from .helpers import FeedImporter
  
@receiver(post_save, sender=Feed)
def saveArticles(sender, instance, created, **kwargs):
  if created:
    FeedImporter.importFeed(instance)
