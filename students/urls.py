"""
URL configuration for students app.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - Path converters (<int:pk>) and Regular Expressions (re_path)
"""

from django.urls import path, re_path
from . import views

app_name = 'students'

urlpatterns = [
    # List all students
    path('', views.student_list_view, name='list'),

    # Create new student (Admin / Faculty)
    path('add/', views.student_create_view, name='create'),

    # Detail view using integer path converter <int:pk>
    path('<int:pk>/', views.student_detail_view, name='detail'),

    # Edit student
    path('<int:pk>/edit/', views.student_update_view, name='edit'),

    # Delete student
    path('<int:pk>/delete/', views.student_delete_view, name='delete'),

    # Regex URL pattern demonstrating INT253 Unit 2: re_path with regular expression
    re_path(r'^reg/(?P<reg_no>[0-9]{4,15})/$', views.student_by_reg_view, name='by_reg'),
]

