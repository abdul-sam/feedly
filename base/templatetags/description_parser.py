import re
from django import template

register = template.Library()

@register.filter
def feed_description(description):
  clean = re.compile('<.*?>')
  description = re.sub(clean, '', description)
  description = re.sub('\n', '', description)
  return re.sub(' +', ' ', description)[0:100]


@register.filter
def article_description(description):
  return description.replace('Continue reading&hellip;', '')


@register.filter
def getFeeds(folder):
  return [ff.feed for ff in folder.folder_feeds.all()]

