from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from src.views import post_imd4,ImageCtmServer

fav_icon = RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('analytics/', include('analytics.urls')),
    path('order/', include('order.urls')),
    path('src/', include('src.urls')),
    path('note/', include('notification.urls')),
    path('voice/', include('voice.urls')),
    path('videos/', include('videos.urls')),
    path('nvs-admin/', include('store.details.ctm_admin.urls')),
    path('support/', include('chat.urls')),
    path('auth/', include('clients.urls')),
    path('blog/', include('blog.urls')),
    path('blog/admin/', include('blog.details.blog_admin.urls')),
    path('sd/', include('store.details.categories.urls')),
    path('search/', include('store.details.search.urls')),
    path('nvs-seller/', include('store.details.seller.urls')),
    path('e/', include('draggables.urls')),
    path('n/', include('utils.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^favicon\.ico$', fav_icon),
    # re_path(r'^media/categories/uploads/(?P<path>.*)$', post_imd4),
    # re_path(r'^media/categories/uploads/(?P<path>.*)$', ImageCtmServer),
    # re_path(r'^media/categories/uploads/(?P<path>.*)/(?P<username>\w+)?._s_h(?P<height>\d+)?_w(?P<width>\d+)?$', ImageCtmServer),
    re_path(r'^media/(?P<path>.*)$', ImageCtmServer),
    # re_path(r'^media/(?P<path>.*)$', post_imd4),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)