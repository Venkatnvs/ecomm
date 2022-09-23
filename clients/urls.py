from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', Registration.as_view(), name='just-auth' ),
    path('register/', Registration.as_view(), name='register' ),
    path('login/', Login.as_view(), name='login' ),
    path('logout/', Logout.as_view(), name='logout' ),
    path('reset-password', ResetPassword.as_view(), name='reset-password' ),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name='validate-email'),
    path('activate-user/<uidb64>/<token>', Verification.as_view(), name='activate'),
    path('reset-user-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='reset-user-password')
]