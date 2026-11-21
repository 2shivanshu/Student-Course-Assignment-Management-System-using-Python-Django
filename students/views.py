"""
Function-Based Views for Students App.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - FBVs, Path Converters (<int:pk>), HTTP Methods
Unit 5: Models & ORM - CRUD operations, QuerySet filtering
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Student
from .forms import StudentForm


def student_list_view(request):
    """
    List all students with search and department filtering.
    Demonstrates:
    - GET parameter parsing (request.GET.get)
    - Django ORM filter, Q objects, order_by
    - Dynamic context passed to template
    """
    search_query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('department', '').strip()

    students = Student.objects.all()

    # Search filter by Name or Registration Number
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Department filter
    if dept_filter:
        students = students.filter(department=dept_filter)

    context = {
        'students': students,
        'total_count': students.count(),
        'search_query': search_query,
        'dept_filter': dept_filter,
        'departments': Student.DEPARTMENT_CHOICES,
        'page_title': 'Registered Students Directory',
    }
    return render(request, 'students/student_list.html', context)


def student_detail_view(request, pk):
    """
    Display single student profile, enrolled courses, and past submissions.
    Demonstrates:
    - Path converter <int:pk>
    - get_object_or_404 error handling
    - Reverse relationship navigation (student.enrolled_courses, student.submissions)
    """
    student = get_object_or_404(Student, pk=pk)
    enrolled_courses = student.enrolled_courses.all()
    submissions = student.submissions.select_related('assignment', 'assignment__course').all()

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'submissions': submissions,
        'page_title': f"Student: {student.name}",
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def student_create_view(request):
    """
    Create a new student record manually (Admin / Faculty).
    Demonstrates:
    - ModelForm rendering and validation
    - POST-Redirect-GET pattern
    - Django messages framework
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only faculty or administrators can add student records.")
        return redirect('students:list')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student = form.save()
            messages.success(request, f"Student '{new_student.name}' ({new_student.registration_number}) was created successfully!")
            return redirect('students:detail', pk=new_student.pk)
        else:
            messages.error(request, "Please check and correct the errors below.")
    else:
        form = StudentForm()

    context = {
        'form': form,
        'is_edit': False,
        'page_title': 'Add New Student Record',
    }
    return render(request, 'students/student_form.html', context)


@login_required
def student_update_view(request, pk):
    """
    Update existing student record.
    Demonstrates:
    - Fetching instance with get_object_or_404
    - Pre-populating ModelForm with instance
    - Authorization check (staff or self)
    """
    student = get_object_or_404(Student, pk=pk)

    # Permission: Only staff or the student themselves can edit
    is_owner = (request.user.is_authenticated and hasattr(request.user, 'student_profile') and request.user.student_profile.pk == student.pk)
    if not (request.user.is_staff or request.user.is_superuser or is_owner):
        messages.error(request, "You do not have authorization to edit this student profile.")
        return redirect('students:detail', pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile for '{student.name}' updated successfully.")
            return redirect('students:detail', pk=student.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
        'is_edit': True,
        'page_title': f"Edit Student: {student.name}",
    }
    return render(request, 'students/student_form.html', context)


@login_required
def student_delete_view(request, pk):
    """
    Delete student record.
    Demonstrates:
    - Safe deletion via POST confirmation
    - Staff permission check
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only administrators can remove student records.")
        return redirect('students:list')

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student_name = student.name
        student.delete()
        messages.success(request, f"Student record for '{student_name}' has been permanently deleted.")
        return redirect('students:list')

    context = {
        'student': student,
        'page_title': f"Confirm Deletion: {student.name}",
    }
    return render(request, 'students/student_confirm_delete.html', context)


def student_by_reg_view(request, reg_no):
    """
    Lookup Student by Registration Number.
    Demonstrates INT253 Unit 2: Regular Expression URL routing using re_path().
    The URL matches registration numbers with regex r'^[0-9]{4,15}$'.
    """
    student = get_object_or_404(Student, registration_number=reg_no)
    return redirect('students:detail', pk=student.pk)

