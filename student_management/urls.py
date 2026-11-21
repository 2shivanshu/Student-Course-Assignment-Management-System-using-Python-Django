"""
URL configuration for student_management project.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - URL patterns, includes, error handling
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    # Django Admin site (Unit 5: Django Admin)
    path('admin/', admin.site.urls),

    # Public Landing Page (Home)
    path('', account_views.home_view, name='home'),

    # Student Dashboard (Unit 6: Authenticated Dashboard)
    path('dashboard/', account_views.student_dashboard_view, name='dashboard'),

    # Admin / Faculty Dashboard
    path('admin-dashboard/', account_views.admin_dashboard_view, name='admin_dashboard'),

    # App-level URL delegations using include()
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignments.urls')),
]

# Error Handlers (Unit 2: Error Handling)
handler404 = 'accounts.views.custom_404_view'
handler500 = 'accounts.views.custom_500_view'

# Serve uploaded media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

