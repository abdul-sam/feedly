from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Board, Category, Feed
from .forms import BoardForm, CategoryForm, FeedForm
import feedparser

from .helpers import CategoryFeed, ImageParser

def home(request):
  # feed = feedparser.parse('https://feeds.arstechnica.com/arstechnica/technology-lab')
  # items = feed.entries
  # titles = []
  # for item in items:
  #     titles.append(item.title)
  # return HttpResponse(len(titles))
  category_form = CategoryForm()
  feed_form = FeedForm()
  board_form = BoardForm()
  total_feeds = CategoryFeed.total_feed_count
  boards = Board.objects.all()

  categories = Category.objects.all()
  context = { 'categories': categories, 'category_form': category_form, 
             'feed_form': feed_form, 'board_form': board_form, 
             'total_feeds': total_feeds, 'boards': boards }
  return render(request, 'home.html', context)


def newCategory(request):
  form = CategoryForm()
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      name = request.POST.get('name')
      Category.objects.create(name=name)
      return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


def newFeed(request):
  form = FeedForm()
  if request.method == 'POST':
    title, description, image_url = '', '', ''
    category_name = request.POST.get('category')
    category, created = Category.objects.get_or_create(name=category_name)
    feed_url = request.POST.get('feed_url')
    feed = feedparser.parse(feed_url)
    if len(feed.entries) > 0:
      if feed.channel is not None:
        title = feed.channel.title
        if hasattr(feed.channel, 'description'):
          description = feed.channel.description
        if hasattr(feed.channel, 'image'):
          image_url = feed.channel.image.url
        elif hasattr(feed.channel, 'icon'):
          image_url = feed.channel.icon

    Feed.objects.create(
      title = title,
      description = description,
      image_url = image_url,
      feed_url = feed_url,
      category = category
    )

    CategoryFeed.feedCount(category)
    return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


def singleFeed(request, pk):
  feed = Feed.objects.get(pk=pk)
  category_form = CategoryForm()
  feed_form = FeedForm()
  board_form = BoardForm()
  total_feeds = CategoryFeed.total_feed_count
  boards = Board.objects.all()

  categories = Category.objects.all()
  if feed is not None:
    parsed_feed = feedparser.parse(feed.feed_url)
    feed_count = len(parsed_feed.entries)
    feeds = parsed_feed.entries
    images = {}
    for f in feeds:
      src = ImageParser.parseImage(f)
      if src != '':
        images[f.link] = src[1:-1]

    context = { 'title': feed.title, 'parsed_feed': parsed_feed, 
               'categories': categories, 'category_form': category_form, 
               'feed_form': feed_form, 'board_form': board_form, 
               'feed_count': feed_count, 'feeds': feeds, 'images': images, 
               'total_feeds': total_feeds, 'boards': boards}
    return render(request, 'feed.html', context)
  
  context = {'categories': categories, 'category_form': category_form, 'feed_form': feed_form}
  return render(request, 'home.html', context)


def singleCategory(request, pk):
  category = Category.objects.get(pk=pk)
  category_form = CategoryForm()
  feed_form = FeedForm()
  board_form = BoardForm()
  total_feeds = CategoryFeed.total_feed_count
  boards = Board.objects.all()

  categories = Category.objects.all()
  if category is not None:
    feeds = []
    images = {}
    for f in category.feeds.all():
      parsed_feed = feedparser.parse(f.feed_url)
      for feed in parsed_feed.entries:
        src = ImageParser.parseImage(feed)
        if src != '':
          images[feed.link] = src[1:-1]

        feeds.append(feed)
      
    feed_count = len(feeds)

    context = { 'title': category.name, 'categories': categories, 
               'category_form': category_form, 'feed_form': feed_form, 
               'board_form': board_form, 'feed_count': feed_count, 'feeds': feeds, 
               'images': images, 'total_feeds': total_feeds, 'boards': boards}
    return render(request, 'category.html', context)
  
  context = {'categories': categories, 'category_form': category_form, 'feed_form': feed_form}
  return render(request, 'home.html', context)


def newBoard(request):
  form = BoardForm()
  if request.method == 'POST':
    form = BoardForm(request.POST)
    if form.is_valid():
      title = request.POST.get('title')
      description = request.POST.get('description')
      public = request.POST.get('public') if request.POST.get('public') is not None else False
      Board.objects.create(
        title = title,
        description = description,
        public = public
      )
      return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)