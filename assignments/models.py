"""
Database models for Assignments and Submissions.

INT253: Web Development in Python Using Django
Unit 5: Models, ForeignKey, Constraints, and ORM
"""

from django.db import models
from django.utils import timezone
from courses.models import Course
from students.models import Student


class Assignment(models.Model):
    """
    Assignment Model representing course tasks created by faculty/admin.
    Fields:
    - Assignment Title
    - Description / Instructions
    - Course (ForeignKey to Course)
    - Deadline (Due datetime)
    - Max Marks (Grading scale)
    """
    assignment_title = models.CharField(
        max_length=200,
        verbose_name="Assignment Title",
        help_text="Title of the assignment or practical project task"
    )

    description = models.TextField(
        verbose_name="Description / Instructions",
        help_text="Detailed problem statement and submission instructions"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Associated Course"
    )

    deadline = models.DateTimeField(
        verbose_name="Submission Deadline",
        help_text="Date and time when submissions close"
    )

    max_marks = models.PositiveIntegerField(
        default=100,
        verbose_name="Maximum Marks",
        help_text="Total marks allocated for this assignment"
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
        ordering = ['deadline', '-created_at']
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

    def __str__(self):
        return f"{self.assignment_title} ({self.course.course_code})"

    @property
    def is_past_due(self):
        """Returns True if the assignment deadline has elapsed."""
        return timezone.now() > self.deadline

    def get_total_submissions(self):
        """Total number of student submissions received for this assignment."""
        return self.submissions.count()

    def get_graded_submissions(self):
        """Count of submissions that have been assessed."""
        return self.submissions.filter(status='Graded').count()


class Submission(models.Model):
    """
    Submission Model representing student work submitted for an assignment.
    Fields:
    - Student: ForeignKey to Student
    - Assignment: ForeignKey to Assignment
    - Submission Date: auto_now_add=True
    - Submission Text: Student's answer or project repository link
    - Attachment: Optional file upload
    - Status: 'Submitted', 'Late', 'Graded'
    - Marks Obtained: Numerical grade assigned by faculty
    - Feedback: Qualitative remarks from reviewer
    """
    STATUS_CHOICES = [
        ('Submitted', 'Submitted On Time'),
        ('Late', 'Submitted Late'),
        ('Graded', 'Evaluated & Graded'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Student"
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Assignment"
    )

    submission_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submission Date & Time"
    )

    submission_text = models.TextField(
        verbose_name="Submission Content",
        help_text="Enter your solution, code snippets, notes, or repository link"
    )

    attachment = models.FileField(
        upload_to='submissions/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Attachment File (Optional)"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Submitted',
        verbose_name="Submission Status"
    )

    marks_obtained = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Marks Obtained"
    )

    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name="Instructor Feedback"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )

    class Meta:
        ordering = ['-submission_date']
        # Ensure a student can only submit once per assignment (can be edited/resubmitted)
        unique_together = ('student', 'assignment')
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return f"{self.student.name} - {self.assignment.assignment_title} [{self.status}]"

    def save(self, *args, **kwargs):
        """
        Auto-determine 'Late' status upon submission if current time is past deadline
        and status has not been marked Graded.
        """
        if not self.pk and self.assignment:
            if timezone.now() > self.assignment.deadline and self.status != 'Graded':
                self.status = 'Late'
        super().save(*args, **kwargs)

