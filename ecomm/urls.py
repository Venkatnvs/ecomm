from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from src.views import post_imd4

fav_icon = RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('order/', include('order.urls')),
    path('src/', include('src.urls')),
    path('note/', include('notification.urls')),
    path('voice/', include('voice.urls')),
    path('videos/', include('videos.urls')),
    path('nvs-admin/', include('store.admin_urls')),
    path('support/', include('chat.urls')),
    path('auth/', include('clients.urls')),
    path('blog/', include('blog.urls')),
    path('e/', include('draggables.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^favicon\.ico$', fav_icon),
    # re_path(r'^media/categories/uploads/(?P<path>.*)$', post_imd4),
    # re_path(r'^media/(?P<path>.*)$', post_imd4),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)