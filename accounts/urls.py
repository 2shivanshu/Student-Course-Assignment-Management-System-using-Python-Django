"""
URL configuration for accounts app.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - App routing, namespacing
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('session-cookie-demo/', views.session_cookie_demo_view, name='session_cookie_demo'),
]

