import json
from rest_framework.response import Response
from .serializers import CategorySerializer, FeedSerializer

class UpdateObject:

  def getJsonValue(request, key):
    data = json.loads(request.body.decode('utf-8'))
    print("Data: ", data)
    return eval(data[key])

  
  def updateFavorite(request, obj):
    favorite = UpdateObject.getJsonValue(request, 'favorite')
    obj.favorit = not favorite
    obj.save()
    categories = request.user.categories.filter(favorit=True)
    categories = CategorySerializer(categories, many=True)
    feeds = request.user.feeds.filter(favorit=True)
    feeds = FeedSerializer(feeds, many=True)
    context = { 'feeds': feeds.data, 'categories': categories.data, 
               'success': True, 'favorite': obj.favorit}
    return Response(context)
  
  def updateReadLater(request, article):
    read_later = UpdateObject.getJsonValue(request, 'readLater')
    print("Read Later: ",read_later)
    article.read_later = not read_later
    article.save()
    context = { 'success': True, 'read_later': article.read_later}
    return Response(context)
  
  def updateRecentlyRead(request, article):
    recently_read = UpdateObject.getJsonValue(request, 'recentlyRead')
    article.recently_read = not recently_read
    article.save()
    context = { 'success': True, 'recently_read': article.recently_read}
    return Response(context)