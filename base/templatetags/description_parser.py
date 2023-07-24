import re
from django import template

register = template.Library()

@register.filter
def parse_description(description):
  clean = re.compile('<.*?>')
  description = re.sub(clean, '', description)
  description = re.sub('\n', '', description)
  return re.sub(' +', ' ', description)[0:100]

