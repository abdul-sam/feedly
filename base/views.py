import feedparser
from django.shortcuts import render, redirect
from .models import Article, Board, Category, Feed, Folder
from .forms import BoardForm, CategoryForm, FeedForm, FolderForm, SignUpForm, UserForm

from .helpers import CategoryFeed, FeedArticle, FeedImporter, ViewContext

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
  feeds = Feed.objects.all()
  context = ViewContext.contextView(request.user)
  context.update({'feeds': feeds})
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def newCategory(request):
  form = CategoryForm()
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      name = request.POST.get('name')
      Category.objects.create(
        name = name,
        user = request.user
      )
      return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


@login_required(login_url='login')
def newFolder(request):
  form = FolderForm()
  if request.method == 'POST':
    form = FolderForm(request.POST)
    if form.is_valid():
      name = request.POST.get('name')
      Folder.objects.create(
        name = name,
        user = request.user
      )
      return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


@login_required(login_url='login')
def newFeed(request):
  form = FeedForm()
  if request.method == 'POST':
    user = request.user
    category_name = request.POST.get('category')
    category, created = user.categories.get_or_create(name=category_name)
    feed_url = request.POST.get('feed_url')
    feed = feedparser.parse(feed_url)
    db_feed = FeedArticle.addFeed(feed, feed_url, category, user)
    CategoryFeed.feedCount(category)
    for article in feed.entries:
      FeedArticle.addArticle(article, db_feed, user)
      
    return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


@login_required(login_url='login')
def singleFeed(request, pk):
  user = request.user
  feed = user.feeds.get(pk=pk)
  context = ViewContext.contextView(user)

  if feed is not None:
    feed_count = feed.articles.count()
    articles = feed.articles.all()

    obj = { 'id': feed.id, 'type': 'feed', 'favorite': feed.favorit }

    feed_context = { 'title': feed.title, 'feed_count': feed_count, 
                    'articles': articles, 'obj': obj}
    
    context.update(feed_context)
    return render(request, 'feed.html', context)
  
  return render(request, 'home.html', context)


@login_required(login_url='login')
def singleCategory(request, pk):
  user = request.user
  category = user.categories.get(pk=pk)
  context = ViewContext.contextView(user)

  if category is not None:
    feed_ids = [f.id for f in category.feeds.all()]
    articles = Article.objects.filter(feed__in=feed_ids).distinct()
    feed_count = articles.count()
    obj = {'id': category.id, 'type': 'category', 'favorite': category.favorit}

    feed_context = { 'title': category.name, 'feed_count': feed_count, 
                    'articles': articles, 'obj': obj }
    context.update(feed_context)
    return render(request, 'category.html', context)
  
  return render(request, 'home.html', context)


@login_required(login_url='login')
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
        public = public,
        user = request.user
      )
      return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


@login_required(login_url='login')
def categoryList(request):
  user = request.user
  context = ViewContext.contextView(user)

  category_ids = [c.id for c in user.categories.all()]
  feed_ids = [f.id for f in Feed.objects.filter(category__in=category_ids)]
  articles = Article.objects.filter(feed__in=feed_ids).distinct()
  feed_count = articles.count()
  obj = {'id': user.pk, 'type': 'all'}

  feed_context = { 'title': 'All Personal Feeds', 'feed_count': feed_count, 
                  'articles': articles, 'obj': obj }
  context.update(feed_context)
  return render(request, 'category_list.html', context)


@login_required(login_url='login')
def article(request, category_pk, feed_pk, pk):
  user = request.user
  context = ViewContext.contextView(user)
  article = user.articles.get(pk=pk)

  article_context = {'article': article}
  context.update(article_context)
  return render(request, 'article.html', context)


@login_required(login_url='login')
def readLater(request):
  user = request.user
  context = ViewContext.contextView(user)
  articles = user.articles.filter(read_later=True)

  article_context = {'articles': articles, 'title': 'Read Later'}
  context.update(article_context)
  return render(request, 'read.html', context)

@login_required(login_url='login')
def recentlyRead(request):
  user = request.user
  context = ViewContext.contextView(user)
  articles = user.articles.filter(recently_read=True)

  article_context = {'articles': articles, 'title': 'Recently Read'}
  context.update(article_context)
  return render(request, 'read.html', context)


def importFeed(request, pk):
  print("ID: ", pk)
  feed = Feed.objects.get(pk=pk)
  if feed is not None:
    FeedImporter.importFeed(feed)

  return redirect('adminFeedUrl')

def adminFeedUrl(request):
  pass