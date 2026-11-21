"""
Forms for students app.

INT253: Web Development in Python Using Django
Unit 4: ModelForm and Server-side Field Validation
"""

import re
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    """
    ModelForm for Student CRUD Operations.
    Demonstrates:
    - ModelForm auto-field generation
    - Custom widgets with Bootstrap 5 classes
    - Validation methods clean_phone and clean_registration_number
    """
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'registration_number', 'department', 'join_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Student Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@university.edu'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile Number'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 12200101'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Please provide a valid 10-digit mobile number.")
        return phone

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number', '').strip()
        # If updating an existing student, exclude self from uniqueness check
        query = Student.objects.filter(registration_number=reg_num)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("A student with this registration number is already enrolled.")
        return reg_num

