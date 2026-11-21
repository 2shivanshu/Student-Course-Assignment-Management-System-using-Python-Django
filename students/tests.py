"""
Unit and Integration Tests for Students App.

INT253: Web Development in Python Using Django
Unit 2: Path Converters, Regex Routes, 404 Testing
Unit 4: ModelForm Validations
Unit 5: Model Testing
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from students.forms import StudentForm


class StudentModelAndViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(
            username='staffadmin',
            email='staff@university.edu',
            password='adminpassword'
        )
        self.student = Student.objects.create(
            name='Rohit Gupta',
            email='rohit@university.edu',
            phone='9876501234',
            registration_number='12205555',
            department='CSE'
        )

    def test_student_str_representation(self):
        """Test model __str__ method."""
        self.assertEqual(str(self.student), "12205555 - Rohit Gupta")

    def test_student_list_view(self):
        """Test student directory listing and search filter."""
        response = self.client.get(reverse('students:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rohit Gupta')

        # Test search query
        search_res = self.client.get(reverse('students:list') + '?q=12205555')
        self.assertEqual(search_res.status_code, 200)
        self.assertContains(search_res, 'Rohit Gupta')

    def test_student_detail_view(self):
        """Test student detail view with path converter <int:pk>."""
        response = self.client.get(reverse('students:detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '12205555')

    def test_student_detail_404(self):
        """Test nonexistent student ID returns 404."""
        response = self.client.get(reverse('students:detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_student_regex_route(self):
        """Test INT253 Unit 2: re_path regular expression routing for registration numbers."""
        response = self.client.get(f"/students/reg/{self.student.registration_number}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rohit Gupta')

    def test_student_form_validation_phone_digits(self):
        """Test phone number must be 10 digits."""
        form = StudentForm(data={
            'name': 'Invalid Phone Student',
            'email': 'inv@university.edu',
            'phone': '123',  # Too short
            'registration_number': '12204444',
            'department': 'CSE',
            'join_date': '2026-08-01',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

