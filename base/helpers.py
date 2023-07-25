import feedparser
from django.db.models import Sum
from .models import Board, Category
from .forms import BoardForm, CategoryForm, FeedForm, SignUpForm, UserForm

class CategoryFeed:

  def feedCount(category):
    feed_count = 0
    for f in category.feeds.all():
      parsed_feed = feedparser.parse(f.feed_url)
      feed_count += len(parsed_feed.entries)

    category.total_feed_count = feed_count
    category.save()

  def total_feed_count():
    return Category.objects.aggregate(Sum('total_feed_count'))['total_feed_count__sum']
  


class ImageParser:

  def parseImage(feed):
    src = ''
    if hasattr(feed, 'content'):
      src = feed.content[0].value.split("src=")
    elif hasattr(feed, 'media_thumbnail'):
      src = feed.media_thumbnail[0]['url']
    elif hasattr(feed, 'description'):
      src = feed.description.split("src=")
    
    if len(src) > 1:
      src = src[1].split(" />\n")[0]

    return src
  

class ViewContext:

  def contextView(user):
    board_form = BoardForm()
    category_form = CategoryForm()
    feed_form = FeedForm()
    boards = Board.objects.all()
    categories = Category.objects.all()
    total_feeds = CategoryFeed.total_feed_count

    context = { 'board_form': board_form, 'category_form': category_form, 
             'feed_form': feed_form, 'boards': boards, 
             'categories': categories, 'total_feeds': total_feeds}
    
    return context
  

