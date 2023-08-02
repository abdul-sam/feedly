from django.urls import re_path
from . import views

urlpatterns=[
    re_path(r'^favorite-feed/(?P<pk>\d+)/$', views.favoriteFeed, name='favorite-feed'),
    re_path(r'^favorite-category/(?P<pk>\d+)/$', views.favoriteCategory, name='favorite-category'),
    re_path(r'^boards/(?P<pk>\d+)/add-feed/(?P<feed_pk>\d+)$', views.favoriteCategory, name='board-feed'),
    re_path(r'^article/(?P<pk>\d+)/read-later/$', views.readLaterArticle, name='read-later'),
    re_path(r'^article/(?P<pk>\d+)/$', views.getArticle, name='article'),
    re_path(r'^article/(?P<pk>\d+)/recently-read/$', views.recentlyReadArticle, name='recently-read'),
    re_path(r'^categories/$', views.getCategories, name='api-categories'),
]