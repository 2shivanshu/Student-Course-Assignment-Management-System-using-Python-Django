"""
Admin configuration for students app.

INT253: Web Development in Python Using Django
Unit 5: Django Admin Site Customization
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Customized Admin interface for Student model.
    Demonstrates:
    - list_display: Tabular columns in admin
    - list_filter: Sidebar filters by department and join date
    - search_fields: Search bar matching name, registration number, email
    - ordering: Default sort order
    - fieldsets: Grouping fields with collapsible sections
    - readonly_fields: Non-editable timestamp fields
    """
    list_display = (
        'registration_number',
        'name',
        'department',
        'email',
        'phone',
        'join_date',
        'get_enrolled_courses_count',
        'get_total_submissions_count',
    )

    list_filter = ('department', 'join_date')

    search_fields = ('name', 'registration_number', 'email', 'phone')

    ordering = ('-join_date', 'registration_number')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Account & Identity', {
            'fields': ('user', 'name', 'registration_number')
        }),
        ('Academic Information', {
            'fields': ('department', 'join_date')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone')
        }),
        ('System Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Custom column headers in admin list
    def get_enrolled_courses_count(self, obj):
        return obj.enrolled_courses.count()
    get_enrolled_courses_count.short_description = 'Courses Enrolled'

    def get_total_submissions_count(self, obj):
        return obj.submissions.count()
    get_total_submissions_count.short_description = 'Submissions'

