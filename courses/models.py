"""
Database models for Courses.

INT253: Web Development in Python Using Django
Unit 5: Models, ManyToManyField, and ORM
"""

from django.db import models
from students.models import Student


class Course(models.Model):
    """
    Course Model representing an academic syllabus course.
    Fields:
    - Course Name: e.g., Web Development in Python Using Django
    - Course Code: e.g., INT253 (Unique identifier)
    - Description: Detailed syllabus outline
    - Credits: Credit weight (1 to 5)
    - Department: Offering department
    - Students: ManyToMany relationship representing course enrollments
    """
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('GEN', 'General Education'),
    ]

    course_name = models.CharField(
        max_length=150,
        verbose_name="Course Name",
        help_text="Official title of the subject/course"
    )

    course_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Course Code",
        help_text="Institutional course code (e.g., INT253, CSE301)"
    )

    description = models.TextField(
        verbose_name="Course Description",
        help_text="Syllabus overview and course outcomes"
    )

    credits = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="Credits",
        help_text="Course credit value (typically 1-5)"
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='CSE',
        verbose_name="Department"
    )

    # Many-to-Many Relationship: Multiple students can enroll in multiple courses
    students = models.ManyToManyField(
        Student,
        related_name='enrolled_courses',
        blank=True,
        verbose_name="Enrolled Students"
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
        ordering = ['course_code']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.course_code}: {self.course_name}"

    def get_enrolled_count(self):
        """Returns the number of students enrolled in this course."""
        return self.students.count()

    def get_assignments_count(self):
        """Returns the number of assignments posted for this course."""
        return self.assignments.count()

