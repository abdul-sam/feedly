from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Feed
from .forms import CategoryForm, FeedForm
import feedparser

def home(request):
  # feed = feedparser.parse('https://feeds.arstechnica.com/arstechnica/technology-lab')
  # items = feed.channel.items
  # titles = []
  # for item in items:
  #     titles.append(item.title)
  # return HttpResponse(titles)
  category_form = CategoryForm()
  feed_form = FeedForm()

  categories = Category.objects.all()
  context = { 'categories': categories, 'category_form': category_form, 'feed_form': feed_form }
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
    title, description, image_url = '', 'description', ''
    category_name = request.POST.get('category')
    category, created = Category.objects.get_or_create(name=category_name)
    feed_url = request.POST.get('feed_url')
    feed = feedparser.parse(feed_url)
    print('Feed URL: ', feed_url)
    if feed.channel is not None:
      title = feed.channel.title
      print('Feed Title: ', title)
      description = feed.channel.description
      print('Feed Description: ', description)
      if feed.channel.image is not None:
        image_url = feed.channel.image.url
        print('Feed Image_url: ', image_url)

    Feed.objects.create(
      title = title,
      description = description,
      image_url = image_url,
      feed_url = feed_url,
      category = category
    )
    return redirect('home')
  
  context = { 'form': form }
  return render(request, 'home.html', context)


def singleFeed(request, pk):
  feed = Feed.objects.get(pk=pk)
  category_form = CategoryForm()
  feed_form = FeedForm()

  categories = Category.objects.all()
  if feed is not None:
    parsed_feed = feedparser.parse(feed.feed_url)
    feed_count = len(parsed_feed.channel.title)
    context = { 'feed': feed, 'parsed_feed': parsed_feed, 
               'categories': categories, 'category_form': category_form, 
               'feed_form': feed_form, 'feed_count': feed_count}
    return render(request, 'feed.html', context)
  
  context = {'categories': categories, 'category_form': category_form, 'feed_form': feed_form}
  return render(request, 'home.html', context)