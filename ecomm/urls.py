"""ecomm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('src/', include('src.urls')),
    path('note/', include('notification.urls')),
    path('nvs-admin/', include('store.admin_urls')),
    path('support/', include('chat.urls')),
    path('auth/', include('clients.urls')),
    path('blog/', include('blog.urls')),
    re_path(r'^favicon\.ico$', fav_icon),
    re_path(r'^media/(?P<path>.*)$', post_imd4),
]
# if settings.DEBUG :
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
