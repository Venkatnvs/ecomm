from django.shortcuts import render
import feedparser
from blog.models import Blogs

def BlogMain(request):
    return render(request,'blog/main/index.html')

def feedimport(request):
    if request.GET.get('url'):
        url = request.GET['url'] #Getting URL
        try:
            feed = feedparser.parse(url) #Parsing XML data
        except:
            feed = None
    else:
        feed = None
    context = {
    'feed' : feed,
    }
    return render(request, 'blog/reader.html', context)