from django.urls import path
from .views import main, note_test

urlpatterns = [
    path('', main, name='note-index'),
    path('test/<message>/', note_test, name='note-test'),
]
