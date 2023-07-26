from django.urls import path, re_path
from . import views

urlpatterns = [
  path('', views.home, name='home'),

  re_path(r'^login/$', views.userLogin, name='login'),
  re_path(r'^signup/$', views.userSignup, name='signup'),
  re_path(r'^logout/$', views.userLogout, name='logout'),
  re_path(r'^profile/$', views.userProfile, name="profile"),


  re_path(r'^categories/$', views.categoryList, name='categories'),
  re_path(r'^categories/new/$', views.newCategory, name='new_category'),
  re_path(r'^categories/(?P<pk>\d+)/$', views.singleCategory, name='category'),
  re_path(r'^feeds/new/$', views.newFeed, name='new_feed'),
  re_path(r'^feeds/(?P<pk>\d+)/$', views.singleFeed, name='feed'),
  re_path(r'^baords/new/$', views.newBoard, name='new_board'),

  re_path(r'^categories/(?P<category_pk>\d+)/feeds/(?P<feed_pk>\d+)/article/(?P<pk>\d+)/$', views.article, name='article'),
]