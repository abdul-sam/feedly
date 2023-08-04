import feedparser
from django.db.models import Sum
from .models import Article, Board, Category, Feed
from .forms import BoardForm, FeedForm, FolderForm, SignUpForm, UserForm


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

  def feedCount(folder):
    total_article_count = 0

    counts = [ff.feed.article_count for ff in folder.folder_feeds.all()]
    for count in counts:
      total_article_count += count

    folder.total_article_count = total_article_count
    folder.save()

  def total_feed_count(user):
    feed_count = user.folders.aggregate(Sum('total_article_count'))['total_article_count__sum']
    total_article_count = feed_count if feed_count is not None else 0
    return total_article_count


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

  def getImage(data):
    src = data.split("src=")
    src = src[1].split('"')[1] if len(src) > 1 else ''

    return src
  

  def parseImage(feed):
    src = ''
    if hasattr(feed, 'content'):
      src = ImageParser.getImage(feed.content[0].value)
    elif hasattr(feed, 'media_thumbnail'):
      src = feed.media_thumbnail[0]['url']
    elif hasattr(feed, 'description'):
      src = ImageParser.getImage(feed.description)

    return src


class ViewContext:

  def contextView(user):
    board_form = BoardForm()
    folder_form = FolderForm()
    feed_form = FeedForm()

    boards = user.boards.all()
    folders = user.folders.all()
    total_feeds = CategoryFeed.total_feed_count(user)

    favorite_feeds = [f.feed for f in user.favorites.filter(favorite_type='Feed')]
    favorite_folders = [f.feed for f in user.favorites.filter(favorite_type='Folder')]

    context = { 'board_form': board_form, 'folder_form': folder_form, 
             'feed_form': feed_form, 'boards': boards, 
             'folders': folders, 'total_feeds': total_feeds,
             'favorite_feeds': favorite_feeds, 'favorite_folders': favorite_folders}
    
    return context
  

