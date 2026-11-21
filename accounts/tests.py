"""
Unit and Integration Tests for Accounts & Authentication App.

INT253: Web Development in Python Using Django
Unit 3: Basic Django Tests & View Verification
Unit 6: Authentication & Sessions Testing
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student


class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='teststudent',
            email='teststudent@university.edu',
            password='testpassword123'
        )
        self.student = Student.objects.create(
            user=self.user,
            name='Test Student',
            email='teststudent@university.edu',
            phone='9876543210',
            registration_number='12208888',
            department='CSE'
        )

    def test_home_page_status_and_template(self):
        """Test landing page loads with status 200 and uses correct template."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Student Course & Assignment Management System')


    def test_login_successful(self):
        """Test authentication with correct credentials."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'teststudent',
            'password': 'testpassword123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_credentials(self):
        """Test login fails gracefully with wrong password."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'teststudent',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Invalid username or password')

    def test_logout_view(self):
        """Test logout flushes user session."""
        self.client.login(username='teststudent', password='testpassword123')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_student_dashboard_requires_login(self):
        """Test unauthenticated user is redirected to login page from dashboard."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_student_registration_validation(self):
        """Test registration creates User and Student records."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newregstudent',
            'email': 'newreg@university.edu',
            'password': 'safePassword123',
            'confirm_password': 'safePassword123',
            'name': 'New Registered Student',
            'registration_number': '12207777',
            'phone': '9123456789',
            'department': 'IT',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newregstudent').exists())
        self.assertTrue(Student.objects.filter(registration_number='12207777').exists())

    def test_session_cookie_demo_page(self):
        """Test session cookie demo page loads and increments session counter."""
        response = self.client.get(reverse('accounts:session_cookie_demo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/session_cookie_demo.html')

        # Test increment action
        post_response = self.client.post(reverse('accounts:session_cookie_demo'), {
            'action': 'increment_session'
        }, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(self.client.session.get('lab_counter'), 1)
