from django import template
from datetime import datetime

register = template.Library()

def RssDate(value):
    return datetime.fromisoformat(value)
register.filter('rssdate', RssDate)