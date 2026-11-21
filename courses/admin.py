"""
Admin configuration for courses app.

INT253: Web Development in Python Using Django
Unit 5: Django Admin Site Customization
"""

from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Custom Admin for Course model.
    Demonstrates:
    - filter_horizontal for ManyToManyField (students)
    - list_display with computed methods
    - search_fields and list_filter
    """
    list_display = (
        'course_code',
        'course_name',
        'department',
        'credits',
        'get_enrolled_count',
        'get_assignments_count',
        'created_at',
    )

    list_filter = ('department', 'credits', 'created_at')

    search_fields = ('course_code', 'course_name', 'description')

    ordering = ('course_code',)

    filter_horizontal = ('students',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Course Identification', {
            'fields': ('course_code', 'course_name', 'department', 'credits')
        }),
        ('Curriculum Content', {
            'fields': ('description',)
        }),
        ('Student Enrollments', {
            'fields': ('students',)
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_enrolled_count(self, obj):
        return obj.students.count()
    get_enrolled_count.short_description = 'Students Enrolled'

    def get_assignments_count(self, obj):
        return obj.assignments.count()
    get_assignments_count.short_description = 'Assignments'

