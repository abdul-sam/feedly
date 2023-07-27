import json
from rest_framework.response import Response
from .serializers import CategorySerializer, FeedSerializer

class UpdateObject:
    
  def updateFavorite(request, obj):
    data = json.loads(request.body.decode('utf-8'))
    favorite = eval(data['favorite'])
    obj.favorit = not favorite
    obj.save()
    categories = request.user.categories.filter(favorit=True)
    categories = CategorySerializer(categories, many=True)
    feeds = request.user.feeds.filter(favorit=True)
    feeds = FeedSerializer(feeds, many=True)
    context = { 'feeds': feeds.data, 'categories': categories.data, 
               'success': True, 'favorite': obj.favorit}
    return Response(context)