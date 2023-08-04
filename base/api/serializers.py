from rest_framework.serializers import ModelSerializer
from base.models import Article, Category, Feed, Folder, FolderFeed
from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

  def current_user(self):
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      return request.user
      


class FeedSerializer(ModelSerializer):

  class Meta:
    model = Feed
    fields = '__all__'


class CategorySerializer(ModelSerializer):

  feeds = FeedSerializer(many=True)

  class Meta:
    model = Category
    fields = ('id', 'name', 'total_feed_count', 'favorit', 'updated_at', 'created_at', 'feeds')

class ArticleSerializer(ModelSerializer):
  feed = FeedSerializer()
  
  class Meta:
    model = Article
    fields = ('id', 'title', 'description', 'image_url', 'read', 'read_later', 'recently_read', 'link', 'updated_at', 'created_at', 'feed')


class FolderSerializer(ModelSerializer):

  def feeds_folder(self, folder):
    context = []
    for ff in folder.folder_feeds.all():
      feed = {}
      feed['id'] = ff.feed.id
      feed['title'] = ff.feed.title
      feed['article_count'] = ff.feed.article_count
      feed['image_url'] = ff.feed.image_url
      context.append(feed)

    return context

    # return [
    #   (
    #     ff.feed.id,
    #     ff.feed.title,
    #     ff.feed.article_count,
    #     ff.feed.image_url
    #   ) for ff in folder.folder_feeds.all()
    # ]
  
  feeds = serializers.SerializerMethodField('feeds_folder')

  class Meta:
    model = Folder
    fields = ('id', 'name', 'total_article_count', 'feeds')