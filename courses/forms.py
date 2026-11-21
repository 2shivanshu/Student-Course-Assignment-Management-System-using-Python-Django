"""
Forms for courses app.

INT253: Web Development in Python Using Django
Unit 4: Forms, Validation, and Widget Customization
"""

import re
from django import forms
from .models import Course
from students.models import Student


class CourseForm(forms.ModelForm):
    """
    ModelForm for Course Creation and Updating.
    Demonstrates:
    - Custom clean_course_code validation
    - Bootstrap widget styling
    - Integer validation for credits
    """
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'description', 'credits', 'department']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python Django Web Development'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., INT253'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed syllabus and prerequisites'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_course_code(self):
        code = self.cleaned_data.get('course_code', '').strip().upper()
        # Validate alphanumeric course code (3-10 chars)
        if not re.match(r'^[A-Z0-9]{3,10}$', code):
            raise forms.ValidationError("Course code must be 3-10 uppercase alphanumeric characters (e.g., INT253, CSE301).")
        
        # Check uniqueness excluding self
        query = Course.objects.filter(course_code=code)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError(f"Course code '{code}' is already registered.")
        return code


class CourseEnrollmentForm(forms.Form):
    """
    Form to enroll a specific student into a course.
    """
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Select Student --",
        help_text="Select a student to enroll in this course"
    )

