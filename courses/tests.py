"""
Unit and Integration Tests for Courses App.

INT253: Web Development in Python Using Django
Unit 2: Regex Routing (re_path)
Unit 5: ManyToMany ORM Relations
Unit 6: Cookie Handling in Views
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course
from students.models import Student


class CourseModelAndViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='coursestudent',
            email='cstudent@university.edu',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.user,
            name='Course Student',
            email='cstudent@university.edu',
            phone='9876543210',
            registration_number='12203333',
            department='CSE'
        )
        self.course = Course.objects.create(
            course_name='Data Structures & Algorithms',
            course_code='CSE201',
            description='Trees, graphs, dynamic programming, and asymptotic analysis.',
            credits=4,
            department='CSE'
        )

    def test_course_str_representation(self):
        """Test Course model __str__."""
        self.assertEqual(str(self.course), "CSE201: Data Structures & Algorithms")

    def test_course_list_view(self):
        """Test courses catalog page."""
        response = self.client.get(reverse('courses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CSE201')

    def test_course_detail_and_cookie_set(self):
        """Test course detail view sets the last_viewed_course cookie (Unit 6: Cookies)."""
        response = self.client.get(reverse('courses:detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('last_viewed_course', response.cookies)
        self.assertEqual(response.cookies['last_viewed_course'].value, 'CSE201')

    def test_course_regex_by_code(self):
        """Test INT253 Unit 2: re_path regex matching for course codes."""
        response = self.client.get('/courses/code/CSE201/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Data Structures &amp; Algorithms')

    def test_student_enrollment_and_unenrollment(self):
        """Test Many-to-Many course enrollment and unenrollment via POST."""
        self.client.login(username='coursestudent', password='password123')

        # 1. Enroll
        enroll_url = reverse('courses:enroll', kwargs={'pk': self.course.pk})
        res = self.client.post(enroll_url, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.course.students.filter(pk=self.student.pk).exists())
        self.assertEqual(self.course.get_enrolled_count(), 1)

        # 2. Unenroll
        unenroll_url = reverse('courses:unenroll', kwargs={'pk': self.course.pk})
        res2 = self.client.post(unenroll_url, follow=True)
        self.assertEqual(res2.status_code, 200)
        self.assertFalse(self.course.students.filter(pk=self.student.pk).exists())
        self.assertEqual(self.course.get_enrolled_count(), 0)

