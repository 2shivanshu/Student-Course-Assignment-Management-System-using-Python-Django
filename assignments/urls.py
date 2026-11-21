"""
URL configuration for assignments app.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - Path converters and routing
"""

from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    # Assignment catalog
    path('', views.assignment_list_view, name='list'),

    # Create assignment (Faculty)
    path('add/', views.assignment_create_view, name='create'),

    # Assignment detail
    path('<int:pk>/', views.assignment_detail_view, name='detail'),

    # Edit assignment
    path('<int:pk>/edit/', views.assignment_update_view, name='edit'),

    # Delete assignment
    path('<int:pk>/delete/', views.assignment_delete_view, name='delete'),

    # Submit assignment (Student)
    path('<int:pk>/submit/', views.assignment_submit_view, name='submit'),

    # Grade submission (Faculty)
    path('submissions/<int:pk>/grade/', views.submission_grade_view, name='grade'),
]

