"""
Admin configuration for assignments app.

INT253: Web Development in Python Using Django
Unit 5: Django Admin Site Customization
"""

from django.contrib import admin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Custom Admin for Assignment model.
    """
    list_display = (
        'assignment_title',
        'course',
        'deadline',
        'max_marks',
        'get_total_submissions',
        'get_graded_submissions',
        'is_past_due_display',
    )

    list_filter = ('course', 'deadline')

    search_fields = ('assignment_title', 'description', 'course__course_code', 'course__course_name')

    ordering = ('deadline',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Assignment Details', {
            'fields': ('course', 'assignment_title', 'description')
        }),
        ('Deadlines & Scoring', {
            'fields': ('deadline', 'max_marks')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    def is_past_due_display(self, obj):
        return obj.is_past_due
    is_past_due_display.boolean = True
    is_past_due_display.short_description = 'Past Due?'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Custom Admin for Submission model.
    """
    list_display = (
        'student',
        'assignment',
        'submission_date',
        'status',
        'marks_obtained',
        'has_attachment',
    )

    list_filter = ('status', 'submission_date', 'assignment__course')

    search_fields = (
        'student__name',
        'student__registration_number',
        'assignment__assignment_title',
        'submission_text',
    )

    ordering = ('-submission_date',)

    readonly_fields = ('submission_date', 'updated_at')

    fieldsets = (
        ('Submission Metadata', {
            'fields': ('student', 'assignment', 'submission_date', 'status')
        }),
        ('Student Solution', {
            'fields': ('submission_text', 'attachment')
        }),
        ('Evaluation & Feedback', {
            'fields': ('marks_obtained', 'feedback')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('updated_at',)
        }),
    )

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'Attachment Attached'

