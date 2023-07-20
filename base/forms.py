from django.forms import ModelForm
from .models import Category, Feed

class CategoryForm(ModelForm):
  class Meta:
    model = Category
    fields = '__all__'
    exclude = ['total_feed_count']


class FeedForm(ModelForm):
  class Meta:
    model = Feed
    fields = '__all__'
    exclude = ['title', 'description', 'image_url']