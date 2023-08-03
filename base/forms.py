from typing import Any
from django.forms import ModelForm
from .models import Board, Category, Feed, Folder

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
      # visible.field.widget.attrs['placeholder'] = "Enter {}".format(visible.field.label)

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')


class BoardForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Board
    fields = '__all__'
    exclude = ['public', 'user']


class CategoryForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Category
    fields = '__all__'
    exclude = ['total_feed_count', 'user']


class FolderForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Folder
    fields = '__all__'
    exclude = ['total_article_count', 'user']


class FeedForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Feed
    fields = '__all__'
    exclude = ['title', 'description', 'image_url']


class UserForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = User
    fields = ['first_name', 'last_name']