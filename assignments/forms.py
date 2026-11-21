"""
Forms for assignments app.

INT253: Web Development in Python Using Django
Unit 4: ModelForm, File Uploads, and Custom Field Validation
"""

from django import forms
from django.utils import timezone
from .models import Assignment, Submission


class AssignmentForm(forms.ModelForm):
    """
    ModelForm for Faculty to Create and Edit Course Assignments.
    Demonstrates:
    - HTML5 datetime-local widget
    - Custom validation: deadline must be a future date
    - Max marks bounds validation
    """
    class Meta:
        model = Assignment
        fields = ['course', 'assignment_title', 'description', 'deadline', 'max_marks']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'assignment_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lab 4: Django ORM Queries'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed requirements and instructions'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 100}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        # On creation, verify deadline is in future
        if deadline and not self.instance.pk:
            if deadline < timezone.now():
                raise forms.ValidationError("Assignment deadline must be scheduled in the future.")
        return deadline


class AssignmentSubmissionForm(forms.ModelForm):
    """
    ModelForm for Students to Submit Assignment Solutions.
    Demonstrates:
    - Text solution input
    - File attachment upload (enctype="multipart/form-data")
    - Validation on submission content
    """
    class Meta:
        model = Submission
        fields = ['submission_text', 'attachment']
        widgets = {
            'submission_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Paste your solution code, write your explanatory answers, or provide a GitHub / Google Drive link...'
            }),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_submission_text(self):
        text = self.cleaned_data.get('submission_text', '').strip()
        if len(text) < 10:
            raise forms.ValidationError("Please provide a meaningful submission response (at least 10 characters).")
        return text


class SubmissionGradingForm(forms.ModelForm):
    """
    ModelForm for Faculty to Evaluate Submissions.
    Demonstrates:
    - Grading validation against assignment max_marks
    - Status updating to 'Graded'
    """
    class Meta:
        model = Submission
        fields = ['marks_obtained', 'feedback', 'status']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Constructive feedback for the student...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_marks_obtained(self):
        marks = self.cleaned_data.get('marks_obtained')
        if marks is not None and self.instance and self.instance.assignment:
            max_marks = self.instance.assignment.max_marks
            if marks > max_marks:
                raise forms.ValidationError(f"Marks obtained ({marks}) cannot exceed the maximum allowed ({max_marks}).")
        return marks

