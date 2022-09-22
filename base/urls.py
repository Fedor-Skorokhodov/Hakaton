from django.urls import path
from rest_framework.authtoken import views as views_token
from . import views


urlpatterns = [
    path('auth_get_token', views_token.obtain_auth_token),
]