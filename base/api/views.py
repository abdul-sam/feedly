from rest_framework.decorators import api_view
from .heplers import UpdateObject
from rest_framework.response import Response
from base.models import Category, Feed, Folder, FolderFeed
from .serializers import ArticleSerializer, CategorySerializer, FeedSerializer, FolderSerializer
from django.db.models import Q

from django.contrib.auth.models import User

from base.helpers import CategoryFeed


@api_view(['PUT'])
def favoriteFeed(request, pk):
  user = request.user
  feed = user.feeds.get(pk=pk)
  return UpdateObject.updateFavorite(request, feed)


@api_view(['PUT'])
def favoriteCategory(request, pk):
  user = request.user
  category = user.categories.get(pk=pk)
  return UpdateObject.updateFavorite(request, category)


@api_view(['PUT'])
def readLaterArticle(request, pk):
  article = request.user.articles.get(pk=pk)
  return UpdateObject.updateReadLater(request, article)


@api_view(['PUT'])
def recentlyReadArticle(request, pk):
  article = request.user.articles.get(pk=pk)
  return UpdateObject.updateRecentlyRead(request, article)

@api_view(['GET'])
def getArticle(request, pk):
  article = request.user.articles.get(pk=pk)
  return Response(ArticleSerializer(article).data)


@api_view(['GET'])
def getCategories(request):
  categories = Category.objects.all()
  return Response(CategorySerializer(categories, many=True).data)

@api_view(['GET'])
def getFolders(request):
  folders = Folder.objects.all()
  return Response(FolderSerializer(folders, many=True).data)


@api_view(['GET'])
def getFeeds(request):
  query = request.GET.get('q')
  q = query if query is not None else ''
  feeds = Feed.objects.filter(
    Q(title__icontains=q) |
    Q(description__icontains=q)
  )
  return Response(FeedSerializer(feeds, many=True).data)


@api_view(['PUT'])
def followUnfollowFeed(request, pk, feed_id):
  context = {'follow': True, 'success': True}

  # Temporary block
  user_id = UpdateObject.getJsonValue(request, 'user_id')
  user = User.objects.get(pk=user_id)
  # Temporary block end

  db_feed = Feed.objects.get(pk=feed_id)
  folder = Folder.objects.get(pk=pk)

  folder_feed = FolderFeed.objects.filter(
    folder=pk, 
    feed=feed_id,
    user=user.pk
  )

  if db_feed is not None and folder is not None:
    if folder_feed.count() > 0:
      folder_feed.first().delete()
      context['follow'] = False
    else:
      FolderFeed.objects.create(
        feed=db_feed,
        folder=folder,
        user=user
      )
      context['follow'] = True
    
    CategoryFeed.feedCount(folder)
    folders = Folder.objects.all()
    context.update({
      'folders': FolderSerializer(folders, many=True).data,
      'total_feeds': CategoryFeed.total_feed_count(user)
    })
  else:
    context['sucess'] = False
      
  
  return Response(context)
