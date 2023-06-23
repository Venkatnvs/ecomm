from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/', include('clients.api_urls')),
    path('', Registration.as_view(), name='just-auth' ),
    path('register/', Registration.as_view(), name='register' ),
    path('login/', Login.as_view(), name='login' ),
    path('logout/', Logout.as_view(), name='logout' ),
    path('reset-password', ResetPassword.as_view(), name='reset-password' ),
    path('state-pin', csrf_exempt(states_get_pin), name='state_pin' ),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name='validate-email'),
    path('activate-user/<uidb64>/<token>', Verification.as_view(), name='activate'),
    path('reset-user-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='reset-user-password')
]