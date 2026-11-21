"""
Unit and Integration Tests for Assignments and Submissions App.

INT253: Web Development in Python Using Django
Unit 4: ModelForm Validations & Grading
Unit 5: Models & QuerySet Operations
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from students.models import Student
from courses.models import Course
from assignments.models import Assignment, Submission
from assignments.forms import SubmissionGradingForm


class AssignmentAndSubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(
            username='assignmentstaff',
            email='astaff@university.edu',
            password='staffpass123'
        )
        self.student_user = User.objects.create_user(
            username='submittingstudent',
            email='substudent@university.edu',
            password='studentpass123'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            name='Submitting Student',
            email='substudent@university.edu',
            phone='9876543210',
            registration_number='12201111',
            department='CSE'
        )
        self.course = Course.objects.create(
            course_name='Object Oriented Programming with Java',
            course_code='CSE102',
            description='Inheritance, Polymorphism, Interfaces, and Exception Handling.',
            credits=4,
            department='CSE'
        )
        # Enroll student in course
        self.course.students.add(self.student)

        self.assignment = Assignment.objects.create(
            assignment_title='Lab 1: Polymorphism & Interfaces',
            description='Implement shapes hierarchy with Shape interface and Circle/Rectangle classes.',
            course=self.course,
            deadline=timezone.now() + timedelta(days=5),
            max_marks=100
        )

    def test_assignment_is_not_past_due_initially(self):
        """Test is_past_due property returns False for future deadline."""
        self.assertFalse(self.assignment.is_past_due)

    def test_assignment_list_view(self):
        """Test assignment listing page."""
        response = self.client.get(reverse('assignments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Polymorphism &amp; Interfaces')

    def test_assignment_detail_view(self):
        """Test assignment detail page."""
        response = self.client.get(reverse('assignments:detail', kwargs={'pk': self.assignment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Implement shapes hierarchy')

    def test_student_submission_flow(self):
        """Test student submitting text solution for an assignment."""
        self.client.login(username='submittingstudent', password='studentpass123')
        submit_url = reverse('assignments:submit', kwargs={'pk': self.assignment.pk})

        response = self.client.post(submit_url, {
            'submission_text': 'Here is my complete solution implementing Shape interface and test cases.'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Submission.objects.filter(assignment=self.assignment, student=self.student).exists())
        sub = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertEqual(sub.status, 'Submitted')

    def test_faculty_grading_submission(self):
        """Test faculty evaluation of student submission."""
        # Create submission first
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            submission_text='Student solution ready for grading.',
            status='Submitted'
        )

        self.client.login(username='assignmentstaff', password='staffpass123')
        grade_url = reverse('assignments:grade', kwargs={'pk': submission.pk})

        response = self.client.post(grade_url, {
            'marks_obtained': 92,
            'status': 'Graded',
            'feedback': 'Great code architecture and well structured methods.'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, 'Graded')
        self.assertEqual(submission.marks_obtained, 92)

    def test_grading_form_cannot_exceed_max_marks(self):
        """Test server-side validation rejecting marks greater than assignment max_marks."""
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            submission_text='Student submission.',
            status='Submitted'
        )
        form = SubmissionGradingForm(
            data={'marks_obtained': 150, 'status': 'Graded', 'feedback': 'Exceeding marks'},
            instance=submission
        )
        self.assertFalse(form.is_valid())
        self.assertIn('marks_obtained', form.errors)

