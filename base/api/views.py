from rest_framework.decorators import api_view
from .heplers import UpdateObject
from rest_framework.response import Response
from base.models import Category
from .serializers import ArticleSerializer, CategorySerializer


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