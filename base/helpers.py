import feedparser
from django.db.models import Sum
from .models import Article, Board, Category, Feed
from .forms import BoardForm, CategoryForm, FeedForm, SignUpForm, UserForm


class FeedImporter:
  def importFeed(feed):
    parsed_feed = feedparser.parse(feed.feed_url)
    title, description, image_url = '', '', ''
    article_count = len(parsed_feed.entries)
    if article_count > 0:
      if parsed_feed.channel is not None:
        title = parsed_feed.channel.title
        if hasattr(parsed_feed.channel, 'description'):
          description = parsed_feed.channel.description
        if hasattr(parsed_feed.channel, 'image'):
          image_url = parsed_feed.channel.image.url
        elif hasattr(parsed_feed.channel, 'icon'):
          image_url = parsed_feed.channel.icon
      
      feed.title = title
      feed.description = description
      feed.image_url = image_url
      feed.article_count = article_count
      feed.save()

      for article in parsed_feed.entries:
        FeedArticle.importArticle(article, feed)


class CategoryFeed:

  def feedCount(category):
    feed_count = 0
    for f in category.feeds.all():
      parsed_feed = feedparser.parse(f.feed_url)
      feed_count += len(parsed_feed.entries)

    category.total_feed_count = feed_count
    category.save()

  def total_feed_count(user):
    feed_count = user.categories.aggregate(Sum('total_feed_count'))['total_feed_count__sum']
    total_feed_count = feed_count if feed_count is not None else 0
    return total_feed_count


class FeedArticle:

  def importArticle(article, feed):
    title = article.title
    description = ''
    if hasattr(article, 'description'):
      description = article.description
    elif hasattr(article, 'content'):
      description = article.content

    src = ImageParser.parseImage(article)
    src = src if src != '' else ''

    Article.objects.create(
      title = title,
      description = description,
      image_url = src,
      link = article.link,
      feed = feed
    )


  def addArticle(article, feed, user):
    title = article.title
    description = ''
    if hasattr(article, 'description'):
      description = article.description
    elif hasattr(article, 'content'):
      description = article.content

    src = ImageParser.parseImage(article)
    src = src if src != '' else ''

    Article.objects.create(
      title = title,
      description = description,
      image_url = src,
      link = article.link,
      feed = feed,
      user = user
    )

  def addFeed(parsed_feed, feed_url, category, user):
    title, description, image_url = '', '', ''
    article_count = len(parsed_feed.entries)
    if article_count > 0:
      if parsed_feed.channel is not None:
        title = parsed_feed.channel.title
        if hasattr(parsed_feed.channel, 'description'):
          description = parsed_feed.channel.description
        if hasattr(parsed_feed.channel, 'image'):
          image_url = parsed_feed.channel.image.url
        elif hasattr(parsed_feed.channel, 'icon'):
          image_url = parsed_feed.channel.icon
      
      db_feed = Feed.objects.create(
        title = title,
        description = description,
        image_url = image_url,
        feed_url = feed_url,
        article_count = article_count,
        category = category,
        user = user
      )

      return db_feed



class ImageParser:

  def parseImage(feed):
    src = ''
    if hasattr(feed, 'content'):
      src = feed.content[0].value.split("src=")
      if len(src) > 1:
        src = src[1].split('"')[1]
      else:
        src = ''
    elif hasattr(feed, 'media_thumbnail'):
      src = feed.media_thumbnail[0]['url']
    elif hasattr(feed, 'description'):
      src = feed.description.split("src=")
      if len(src) > 1:
        src = src[1].split('"')[1]

    return src
  

class ViewContext:

  def contextView(user):
    board_form = BoardForm()
    category_form = CategoryForm()
    feed_form = FeedForm()

    boards = user.boards.all()
    categories = user.categories.all()
    total_feeds = CategoryFeed.total_feed_count(user)

    favorite_feeds = user.feeds.filter(favorit=True)
    favorite_categories = user.categories.filter(favorit=True)

    context = { 'board_form': board_form, 'category_form': category_form, 
             'feed_form': feed_form, 'boards': boards, 
             'categories': categories, 'total_feeds': total_feeds,
             'favorite_feeds': favorite_feeds, 'favorite_categories': favorite_categories}
    
    return context
  

