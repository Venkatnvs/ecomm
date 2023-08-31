from django.contrib import admin
from .models import *

admin.site.register(BlogCategories)
admin.site.register(BlogSubCategories)
admin.site.register(Blogs)
admin.site.register(BlogMedia)
admin.site.register(BlogTags)