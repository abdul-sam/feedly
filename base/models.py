from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=200, null=False)
  # user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
  total_feed_count = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  

class Board(models.Model):
  title = models.CharField(max_length=200, null=False)
  description = models.TextField()
  # user = models.ForeignKey(User, related_name='boards', on_delete=models.CASCADE)
  public = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Feed(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_url = models.CharField(max_length=2083)
  feed_url = models.CharField(max_length=2083)
  category = models.ForeignKey(Category, related_name='feeds', on_delete=models.CASCADE)
  board = models.ForeignKey(Board, related_name='feeds', on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
