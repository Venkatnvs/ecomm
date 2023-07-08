from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
import feedparser
from .models import BlogPost

class BlogMain(ListView):
    model = BlogPost
    template_name = 'blog/main/index.html'

class BlogDetail(DetailView):
    model = BlogPost
    template_name = 'blog/main/blog_detail.html'

class BlogCreate(CreateView):
    model = BlogPost
    template_name = 'blog/main/blog_create.html'
    fields = "__all__"

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