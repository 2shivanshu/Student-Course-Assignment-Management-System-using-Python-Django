"""
Forms for accounts app.

INT253: Web Development in Python Using Django
Unit 4: Forms, Validation, and CSRF Protection
"""

import re
from django import forms
from django.contrib.auth.models import User
from students.models import Student


class UserRegistrationForm(forms.Form):
    """
    Combined Registration Form for User Account and Student Profile.
    Demonstrates:
    - Server-side validation via clean_<fieldname>() and clean()
    - Bootstrap widget styling
    - Password confirmation check
    - Regex pattern validation for phone and registration number
    """
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a unique username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@university.edu'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'At least 6 characters'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'})
    )
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'})
    )
    registration_number = forms.CharField(
        max_length=20,
        label="Registration Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12200101'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'})
    )
    department = forms.ChoiceField(
        choices=Student.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number', '').strip()
        if Student.objects.filter(registration_number=reg_num).exists():
            raise forms.ValidationError("A student with this registration number already exists.")
        if len(reg_num) < 4:
            raise forms.ValidationError("Registration number must be at least 4 characters long.")
        return reg_num

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Verify 10-digit phone format
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Phone number must contain exactly 10 numeric digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please verify and retype.")

        return cleaned_data


class UserLoginForm(forms.Form):
    """
    Standard Login Form using Django Authentication.
    Demonstrates form widgets and remember-me checkbox.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form to update student profile details.
    Demonstrates ModelForm and widget overrides.
    """
    class Meta:
        model = Student
        fields = ['name', 'phone', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Phone number must contain exactly 10 numeric digits.")
        return phone


class CookieDemoForm(forms.Form):
    """
    Interactive form for demonstrating setting and reading custom browser cookies.
    """
    theme = forms.ChoiceField(
        choices=[('light', 'Light Mode (Default)'), ('dark', 'Dark Slate Theme'), ('blue', 'University Blue Theme')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    custom_key = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cookie key name (e.g. favorite_subject)'})
    )
    custom_value = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cookie value (e.g. Python Django)'})
    )

