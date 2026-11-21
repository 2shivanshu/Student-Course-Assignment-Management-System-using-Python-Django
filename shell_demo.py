"""
Django Shell & ORM Demonstration Script.

INT253: Web Development in Python Using Django
Unit 5: Models, ORM, QuerySets, and Django Shell Operations

This script demonstrates standard Django ORM commands that can be executed
interactively in the Django Shell:
    python manage.py shell

Or run this file directly:
    python shell_demo.py
"""

import os
import django

# Setup Django standalone environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.utils import timezone
from students.models import Student
from courses.models import Course
from assignments.models import Assignment, Submission
from django.db.models import Count, Avg, Q


def run_orm_demonstration():
    print("=" * 70)
    print("INT253 Unit 5: Django ORM and QuerySet Demonstration")
    print("=" * 70)

    # 1. RETRIEVE ALL (SELECT * FROM students_student)
    print("\n[1] RETRIEVE ALL (Student.objects.all()):")
    all_students = Student.objects.all()
    for s in all_students:
        print(f"    - ID: {s.id} | Reg: {s.registration_number} | Name: {s.name} | Dept: {s.department}")

    # 2. FILTERING & LOOKUPS (WHERE department = 'CSE')
    print("\n[2] FILTERING (Student.objects.filter(department='CSE')):")
    cse_students = Student.objects.filter(department='CSE')
    print(f"    Found {cse_students.count()} CSE students:")
    for s in cse_students:
        print(f"    - {s.name} ({s.registration_number})")

    # 3. FIELD LOOKUPS: icontains, gte, in
    print("\n[3] FIELD LOOKUPS (__icontains, __gte):")
    matching = Student.objects.filter(name__icontains='sharma')
    print(f"    Names containing 'sharma': {[s.name for s in matching]}")

    upcoming_assignments = Assignment.objects.filter(deadline__gte=timezone.now())
    print(f"    Assignments with future deadlines ({upcoming_assignments.count()} found):")
    for a in upcoming_assignments:
        print(f"    - {a.assignment_title} (Due: {a.deadline.strftime('%Y-%m-%d %H:%M')})")

    # 4. SINGLE OBJECT RETRIEVAL (.get() and get_object_or_404)
    print("\n[4] SINGLE OBJECT RETRIEVAL (.get()):")
    try:
        int253 = Course.objects.get(course_code='INT253')
        print(f"    Found course: {int253.course_code} - {int253.course_name} ({int253.credits} credits)")
    except Course.DoesNotExist:
        print("    Course INT253 not found.")

    # 5. RELATIONSHIP TRAVERSING (ForeignKey & ManyToMany)
    print("\n[5] RELATIONSHIP TRAVERSING (Forward and Reverse):")
    if 'int253' in locals():
        # Forward: Assignment -> Course
        first_assign = int253.assignments.first()
        if first_assign:
            print(f"    Assignment '{first_assign.assignment_title}' belongs to course '{first_assign.course.course_name}'")

        # Reverse Many-to-Many: Course -> Enrolled Students
        enrolled = int253.students.all()
        print(f"    Students enrolled in {int253.course_code} ({enrolled.count()} total):")
        for st in enrolled:
            print(f"    - {st.name} ({st.registration_number})")

    # 6. AGGREGATION & ANNOTATION (COUNT, AVG)
    print("\n[6] AGGREGATION & ANNOTATION (Count, Avg):")
    courses_with_counts = Course.objects.annotate(student_count=Count('students')).order_by('-student_count')
    for c in courses_with_counts:
        print(f"    Course: {c.course_code} -> Enrolled Students: {c.student_count}")

    avg_score = Submission.objects.filter(status='Graded').aggregate(Avg('marks_obtained'))
    print(f"    Average Marks across Graded Submissions: {avg_score['marks_obtained__avg']:.1f}")

    # 7. INSERT / CREATE RECORD DEMONSTRATION
    print("\n[7] INSERT OPERATION (Student.objects.create()):")
    demo_reg = "12209999"
    # Clean up previous demo record if exists
    Student.objects.filter(registration_number=demo_reg).delete()

    temp_student = Student.objects.create(
        name="Demo Shell Student",
        email="shell.demo@university.edu",
        phone="9999988888",
        registration_number=demo_reg,
        department="IT",
        join_date=timezone.now().date()
    )
    print(f"    Created new student: ID={temp_student.id}, Name={temp_student.name}, Reg={temp_student.registration_number}")

    # 8. UPDATE RECORD DEMONSTRATION
    print("\n[8] UPDATE OPERATION (instance.save() and QuerySet.update()):")
    temp_student.department = "CSE"
    temp_student.save()
    print(f"    Updated department for ID={temp_student.id}: New Dept={temp_student.department}")

    # 9. DELETE RECORD DEMONSTRATION
    print("\n[9] DELETE OPERATION (instance.delete()):")
    deleted_id = temp_student.id
    temp_student.delete()
    verify_exists = Student.objects.filter(id=deleted_id).exists()
    print(f"    Deleted student ID={deleted_id}. Still in DB? {verify_exists}")

    print("\n" + "=" * 70)
    print("Django ORM demonstration completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    run_orm_demonstration()

