from django.urls import path
from .views import *

urlpatterns= [
    path('help-faq/', HelpPage, name='utils-help-pg'),
    path('contact-page/', ContactPage, name='utils-contact-pg'),
    path('profile/', ProfilePage, name='utils-profile-pg'),
    path('terms-conditions/', TermsConditions, name='utils-terms-conditions-pg'),
    path('log/',ViewLog,name="utils-log")
]