"""
Seed script to populate initial university demonstration data for INT253.
Creates admin accounts, sample students, courses, assignments, and submissions.

Run with:
    python seed_demo_data.py
"""

import os
import django
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from students.models import Student
from courses.models import Course
from assignments.models import Assignment, Submission


def seed_database():
    print("=" * 60)
    print("Seeding Student Course & Assignment Management System Database")
    print("=" * 60)

    # 1. Create Administrator / Faculty User
    admin_user, created = User.objects.get_or_create(username='admin')
    if created or not admin_user.check_password('admin123'):
        admin_user.set_password('admin123')
        admin_user.email = 'admin@university.edu'
        admin_user.first_name = 'Dr. Vikram'
        admin_user.last_name = 'Singh'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("[+] Admin / Faculty account created: admin / admin123")
    else:
        print("[*] Admin account already exists.")

    # 2. Create Student Auth Accounts and Profiles
    students_data = [
        {
            'username': 'student1',
            'password': 'pass123',
            'name': 'Aarav Sharma',
            'email': 'aarav.sharma@university.edu',
            'phone': '9876543210',
            'reg_no': '12200101',
            'dept': 'CSE',
        },
        {
            'username': 'student2',
            'password': 'pass123',
            'name': 'Priya Patel',
            'email': 'priya.patel@university.edu',
            'phone': '9812345678',
            'reg_no': '12200205',
            'dept': 'IT',
        },
        {
            'username': 'student3',
            'password': 'pass123',
            'name': 'Rohan Verma',
            'email': 'rohan.verma@university.edu',
            'phone': '9898989898',
            'reg_no': '12200312',
            'dept': 'CSE',
        },
    ]

    created_students = []
    for s_data in students_data:
        user, u_created = User.objects.get_or_create(username=s_data['username'])
        if u_created or not user.check_password(s_data['password']):
            user.set_password(s_data['password'])
            user.email = s_data['email']
            user.first_name = s_data['name'].split()[0]
            user.last_name = s_data['name'].split()[-1]
            user.is_staff = False
            user.save()

        student, s_created = Student.objects.get_or_create(
            registration_number=s_data['reg_no'],
            defaults={
                'user': user,
                'name': s_data['name'],
                'email': s_data['email'],
                'phone': s_data['phone'],
                'department': s_data['dept'],
                'join_date': timezone.now().date() - timedelta(days=90),
            }
        )
        if not student.user:
            student.user = user
            student.save()

        created_students.append(student)
        print(f"[+] Student created: {student.name} ({student.registration_number}) | Login: {s_data['username']} / {s_data['password']}")

    # 3. Create Courses
    courses_data = [
        {
            'name': 'Web Development in Python Using Django',
            'code': 'INT253',
            'credits': 4,
            'dept': 'CSE',
            'desc': (
                "Comprehensive study of web engineering using Python Django framework.\n"
                "Topics: MVT architecture, views & URL routing, DTL templates, ModelForms,\n"
                "SQLite ORM models, cookies, sessions, authentication, and security."
            ),
        },
        {
            'name': 'Database Management Systems & SQL',
            'code': 'CSE301',
            'credits': 3,
            'dept': 'CSE',
            'desc': (
                "Relational algebra, ER modeling, SQL querying, schema normalization (1NF-3NF/BCNF),\n"
                "transaction management, ACID properties, indexing, and query optimization."
            ),
        },
        {
            'name': 'Cloud Computing and Web Services',
            'code': 'INT306',
            'credits': 3,
            'dept': 'IT',
            'desc': (
                "Cloud service models (IaaS, PaaS, SaaS), virtualization, cloud deployment,\n"
                "containerization with Docker, RESTful APIs, and microservice architectures."
            ),
        },
        {
            'name': 'Embedded Systems & IoT Architectures',
            'code': 'ECE204',
            'credits': 4,
            'dept': 'ECE',
            'desc': (
                "Microcontroller programming, sensor interfacing, wireless telemetry protocols (MQTT, CoAP),\n"
                "and real-time embedded operating systems."
            ),
        },
    ]

    created_courses = {}
    for c_data in courses_data:
        course, c_created = Course.objects.get_or_create(
            course_code=c_data['code'],
            defaults={
                'course_name': c_data['name'],
                'credits': c_data['credits'],
                'department': c_data['dept'],
                'description': c_data['desc'],
            }
        )
        created_courses[course.course_code] = course
        print(f"[+] Course ready: {course.course_code} - {course.course_name}")

    # 4. Enroll Students into Courses
    # Aarav (CSE): INT253, CSE301
    created_courses['INT253'].students.add(created_students[0])
    created_courses['CSE301'].students.add(created_students[0])

    # Priya (IT): INT253, INT306
    created_courses['INT253'].students.add(created_students[1])
    created_courses['INT306'].students.add(created_students[1])

    # Rohan (CSE): INT253, CSE301, INT306
    created_courses['INT253'].students.add(created_students[2])
    created_courses['CSE301'].students.add(created_students[2])
    created_courses['INT306'].students.add(created_students[2])

    print("[+] Student course enrollments configured.")

    # 5. Create Assignments
    assignments_data = [
        {
            'course': created_courses['INT253'],
            'title': 'Lab 1: Django Architecture & Function-Based Views',
            'desc': (
                "Problem Statement:\n"
                "1. Implement Django project setup and register 4 custom applications.\n"
                "2. Create Function-Based Views (FBVs) to handle GET and POST requests.\n"
                "3. Configure URL path converters (<int:pk>) and regex patterns using re_path.\n"
                "4. Submit your source code structure and explanatory notes below."
            ),
            'deadline': timezone.now() + timedelta(days=7),
            'max_marks': 100,
        },
        {
            'course': created_courses['INT253'],
            'title': 'Lab 2: ModelForms & Server-Side Validation',
            'desc': (
                "Problem Statement:\n"
                "1. Build a Student Registration ModelForm with clean_phone() and clean_registration_number().\n"
                "2. Ensure CSRF protection using {% csrf_token %} tag.\n"
                "3. Implement POST-Redirect-GET (PRG) pattern with Django flash messages."
            ),
            'deadline': timezone.now() + timedelta(days=14),
            'max_marks': 100,
        },
        {
            'course': created_courses['INT253'],
            'title': 'Lab 0: Python Environment & Django Installation',
            'desc': (
                "Verify your Python 3 installation, virtual environment setup, and Django packages.\n"
                "Document commands: python -m venv venv, pip install django, django-admin startproject."
            ),
            'deadline': timezone.now() - timedelta(days=4),  # Past Due
            'max_marks': 50,
        },
        {
            'course': created_courses['CSE301'],
            'title': 'Assignment 1: Relational Schema & Normalization',
            'desc': (
                "Convert given business requirements into an Entity-Relationship (ER) model.\n"
                "Normalize relations up to Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF)."
            ),
            'deadline': timezone.now() + timedelta(days=10),
            'max_marks': 100,
        },
    ]

    created_assignments = []
    for a_data in assignments_data:
        assignment, a_created = Assignment.objects.get_or_create(
            assignment_title=a_data['title'],
            course=a_data['course'],
            defaults={
                'description': a_data['desc'],
                'deadline': a_data['deadline'],
                'max_marks': a_data['max_marks'],
            }
        )
        created_assignments.append(assignment)
        print(f"[+] Assignment posted: {assignment.assignment_title} (Due: {assignment.deadline.strftime('%b %d, %Y')})")

    # 6. Create Sample Submissions
    # Aarav submissions:
    # 1. Graded submission for Lab 0
    sub1, _ = Submission.objects.get_or_create(
        student=created_students[0],
        assignment=created_assignments[2],
        defaults={
            'submission_text': (
                "Configured Python 3.12 virtual environment using 'python -m venv env'.\n"
                "Activated environment: .\\env\\Scripts\\activate\n"
                "Installed Django 5+ and verified 'python -m django --version'. Verified SQLite connection."
            ),
            'status': 'Graded',
            'marks_obtained': 48,
            'feedback': 'Excellent explanation of virtual environment isolation and pip dependency management.',
        }
    )

    # 2. Submitted work for Lab 1 (Awaiting grading)
    sub2, _ = Submission.objects.get_or_create(
        student=created_students[0],
        assignment=created_assignments[0],
        defaults={
            'submission_text': (
                "Created student_management project with apps: accounts, students, courses, assignments.\n"
                "Implemented function-based views with HttpResponse and render().\n"
                "Added path converters and regex routing via re_path(r'^reg/(?P<reg_no>[0-9]{4,15})/$')."
            ),
            'status': 'Submitted',
        }
    )

    # Priya submission for Lab 0 (Graded)
    sub3, _ = Submission.objects.get_or_create(
        student=created_students[1],
        assignment=created_assignments[2],
        defaults={
            'submission_text': (
                "Step 1: Installed Python and verified PATH environment.\n"
                "Step 2: Initialized git repository.\n"
                "Step 3: Installed Django framework and ran manage.py check successfully."
            ),
            'status': 'Graded',
            'marks_obtained': 45,
            'feedback': 'Clean setup document. Well done.',
        }
    )

    # Priya submission for Lab 1 (Awaiting grading)
    sub4, _ = Submission.objects.get_or_create(
        student=created_students[1],
        assignment=created_assignments[0],
        defaults={
            'submission_text': (
                "Completed implementation of MVT pattern and URL routing with path converters.\n"
                "Tested GET and POST request flows and verified 404 handler."
            ),
            'status': 'Submitted',
        }
    )

    print("[+] Sample submissions created and linked.")
    print("=" * 60)
    print("Database seeding completed successfully!")
    print("Faculty Login: username='admin', password='admin123'")
    print("Student 1 Login: username='student1', password='pass123'")
    print("Student 2 Login: username='student2', password='pass123'")
    print("Student 3 Login: username='student3', password='pass123'")
    print("=" * 60)


if __name__ == '__main__':
    seed_database()

