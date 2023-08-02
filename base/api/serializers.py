from rest_framework.serializers import ModelSerializer
from base.models import Article, Category, Feed


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
