"""
URL configuration for courses app.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - Path converters and Regular Expressions (re_path)
"""

from django.urls import path, re_path
from . import views

app_name = 'courses'

urlpatterns = [
    # Catalog list
    path('', views.course_list_view, name='list'),

    # Create course (Faculty)
    path('add/', views.course_create_view, name='create'),

    # Course detail by integer primary key
    path('<int:pk>/', views.course_detail_view, name='detail'),

    # Edit course
    path('<int:pk>/edit/', views.course_update_view, name='edit'),

    # Delete course
    path('<int:pk>/delete/', views.course_delete_view, name='delete'),

    # Enroll / Unenroll endpoints
    path('<int:pk>/enroll/', views.course_enroll_view, name='enroll'),
    path('<int:pk>/unenroll/', views.course_unenroll_view, name='unenroll'),

    # Regex URL pattern demonstrating INT253 Unit 2: re_path with course code pattern
    re_path(r'^code/(?P<course_code>[A-Za-z0-9]{3,10})/$', views.course_by_code_view, name='by_code'),
]

