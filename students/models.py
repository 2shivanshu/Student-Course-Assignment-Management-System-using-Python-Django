"""
Database models for Students.

INT253: Web Development in Python Using Django
Unit 5: Models, ORM and Database Management
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    """
    Student Model representing a university student.
    Implements all required fields from course syllabus:
    - Name: Full student name
    - Email: University or personal email
    - Phone: Contact mobile number
    - Registration Number: Unique institutional roll/registration number
    - Department: Academic discipline (e.g., Computer Science, IT)
    - Join Date: Date of admission
    - User: Optional 1-to-1 link with Django's built-in User model for login
    """
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('MBA', 'Management Studies'),
        ('OTHER', 'Other Department'),
    ]

    # One-to-One relationship with Django User for authentication & permissions
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='student_profile',
        help_text="Associated auth account for dashboard login"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Full Name",
        help_text="Student's complete name"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Unique student email address"
    )

    phone = models.CharField(
        max_length=15,
        verbose_name="Contact Number",
        help_text="10-digit mobile number"
    )

    registration_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Registration Number",
        help_text="Unique University Registration ID (e.g. 12200123)"
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='CSE',
        verbose_name="Department"
    )

    join_date = models.DateField(
        default=timezone.now,
        verbose_name="Admission / Join Date"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )

    class Meta:
        ordering = ['-join_date', 'name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.registration_number} - {self.name}"

    def get_enrolled_courses_count(self):
        """Returns the number of courses this student is currently enrolled in."""
        return self.enrolled_courses.count()

    def get_total_submissions_count(self):
        """Returns total assignment submissions made by this student."""
        return self.submissions.count()

