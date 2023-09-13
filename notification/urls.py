from django.urls import path
from .views import *
urlpatterns = [
    path('', main, name='note-index'),
    path('admin/note',SendNotificationAll,name='ctm-admin_allnote')
]
