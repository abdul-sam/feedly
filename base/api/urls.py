from django.urls import re_path
from . import views

urlpatterns=[
    re_path(r'^favorite-feed/(?P<pk>\d+)/$', views.favoriteFeed, name='favorite-feed'),
    re_path(r'^favorite-category/(?P<pk>\d+)/$', views.favoriteCategory, name='favorite-category'),
    re_path(r'^categories/$', views.getCategories, name='api-categories'),
]