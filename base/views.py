from django.shortcuts import render, redirect
from .models import Board, Category, Feed
from .forms import BoardForm, CategoryForm, FeedForm, SignUpForm, UserForm
import feedparser

from .helpers import CategoryFeed, ImageParser

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
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


def userLogin(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Invalid Credentials')

  context = {}
  return render(request, 'accounts/login.html', context)


def userSignup(request):
  form = SignUpForm()
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error was occurred during signup')
      
  context = { 'form': form }
  return render(request, 'accounts/signup.html', context)


def userLogout(request):
  logout(request)
  return redirect('login')


def userProfile(request):
  user = request.user
  form = UserForm(instance=user)

  if request.method == 'POST':
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('profile')
  
  context = {'form': form}
  return render(request, 'accounts/profile.html', context)


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