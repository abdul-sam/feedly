from django import template
from django.template.context import Context as Context

register = template.Library()

@register.filter
def auth(parser):
  nodelist = parser.parse(('endauth', ))
  parser.delete_first_token()
  return AuthNode(nodelist)


class AuthNode(template.Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    output = self.nodelist.render(context)
    return output