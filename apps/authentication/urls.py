# backend/apps/authentication/urls.py

from django.urls import path
from .views import (
    IsSuperuserView,
    CreateAccountView, 
    CreateAccountWithGoogleView, 
    SignInAccountView, 
    ResetPasswordView, 
    ChangePasswordView, 
    GoogleConnectView, 
    GoogleCodeView
)

app_name = 'authentication'

urlpatterns = [
    path('is-superuser/', IsSuperuserView.as_view(), name='is-superuser'),
    path('registration/', CreateAccountView.as_view(), name='registration'),
    path('social-registration/', CreateAccountWithGoogleView.as_view(), name='social-registration'),
    path('sign-in/', SignInAccountView.as_view(), name='sign-in'),  # Agregada barra diagonal al final
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('google-connect/', GoogleConnectView.as_view(), name='google-connect'),
    path('google-code/', GoogleCodeView.as_view(), name='google-code'),
]
