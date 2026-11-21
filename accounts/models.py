"""
Models for the accounts app.

In accordance with INT253 Unit 6 (Authentication & Authorization),
we utilize Django's built-in User model (django.contrib.auth.models.User)
for authentication, credentials, and role permissions (is_staff, is_superuser).
The Student model in the 'students' app maintains a OneToOneField relationship
with this User model.
"""

from django.db import models
from django.contrib.auth.models import User

# Any app-specific account logs or user preferences can be defined here if needed.

