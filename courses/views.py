"""
Function-Based Views for Courses App.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - FBVs, Path Converters, Regex Routes
Unit 5: Models & Many-to-Many ORM Relationships
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from .models import Course
from .forms import CourseForm, CourseEnrollmentForm
from students.models import Student


def course_list_view(request):
    """
    List all available courses with search and department filtering.
    Demonstrates:
    - ORM annotate() to compute student enrollment count per course
    - GET parameter filtering
    - Setting a cookie to remember 'last_course_visited' (Unit 6: Cookies)
    """
    search_query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('department', '').strip()

    courses = Course.objects.annotate(student_count=Count('students')).order_by('course_code')

    if search_query:
        courses = courses.filter(
            Q(course_name__icontains=search_query) |
            Q(course_code__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if dept_filter:
        courses = courses.filter(department=dept_filter)

    # If the user is a logged-in student, check which courses they are already enrolled in
    enrolled_course_ids = []
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        enrolled_course_ids = request.user.student_profile.enrolled_courses.values_list('id', flat=True)

    context = {
        'courses': courses,
        'total_count': courses.count(),
        'search_query': search_query,
        'dept_filter': dept_filter,
        'departments': Course.DEPARTMENT_CHOICES,
        'enrolled_course_ids': list(enrolled_course_ids),
        'page_title': 'Course Curriculum Catalog',
    }
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, pk):
    """
    Display single course details, assignments list, and enrolled students list.
    Demonstrates:
    - Path converter <int:pk>
    - Unit 6: Setting a cookie 'last_viewed_course' in HttpResponse
    """
    course = get_object_or_404(Course, pk=pk)
    assignments = course.assignments.all()
    enrolled_students = course.students.all()

    # Check if current student is enrolled
    is_enrolled = False
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        is_enrolled = course.students.filter(pk=request.user.student_profile.pk).exists()

    context = {
        'course': course,
        'assignments': assignments,
        'enrolled_students': enrolled_students,
        'is_enrolled': is_enrolled,
        'enrollment_form': CourseEnrollmentForm(),
        'page_title': f"{course.course_code}: {course.course_name}",
    }

    # Render template and attach demonstration cookie
    response = render(request, 'courses/course_detail.html', context)
    response.set_cookie('last_viewed_course', f"{course.course_code}", max_age=86400)
    return response


def course_by_code_view(request, course_code):
    """
    Lookup course by Course Code.
    Demonstrates INT253 Unit 2: Regular Expression URL routing using re_path().
    Matches regex r'^code/(?P<course_code>[A-Za-z0-9]{3,10})/$'
    """
    course = get_object_or_404(Course, course_code__iexact=course_code)
    return redirect('courses:detail', pk=course.pk)


@login_required
def course_create_view(request):
    """
    Create a new course (Faculty / Administrator).
    Demonstrates:
    - POST-Redirect-GET pattern
    - ModelForm validation and save()
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied: Only faculty members can create courses.")
        return redirect('courses:list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
            messages.success(request, f"Course '{new_course.course_code}: {new_course.course_name}' created successfully!")
            return redirect('courses:detail', pk=new_course.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CourseForm()

    context = {
        'form': form,
        'is_edit': False,
        'page_title': 'Add New Course',
    }
    return render(request, 'courses/course_form.html', context)


@login_required
def course_update_view(request, pk):
    """
    Update existing course details.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied: Only faculty members can update courses.")
        return redirect('courses:detail', pk=pk)

    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.course_code}' updated successfully.")
            return redirect('courses:detail', pk=course.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
        'course': course,
        'is_edit': True,
        'page_title': f"Edit Course: {course.course_code}",
    }
    return render(request, 'courses/course_form.html', context)


@login_required
def course_delete_view(request, pk):
    """
    Delete a course (Faculty / Administrator).
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied: Only administrators can delete courses.")
        return redirect('courses:detail', pk=pk)

    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        code = course.course_code
        course.delete()
        messages.success(request, f"Course '{code}' and all its assignments were deleted.")
        return redirect('courses:list')

    context = {
        'course': course,
        'page_title': f"Confirm Deletion: {course.course_code}",
    }
    return render(request, 'courses/course_confirm_delete.html', context)


@login_required
def course_enroll_view(request, pk):
    """
    Enroll into a course.
    - If student: enrolls self directly
    - If faculty/staff: enrolls selected student from form
    Demonstrates:
    - Many-to-Many ORM relation: course.students.add(student)
    - Flash messaging and POST-Redirect-GET
    """
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        # Check if logged-in user is a student
        student = getattr(request.user, 'student_profile', None)

        if student:
            # Self-enrollment for student
            if course.students.filter(pk=student.pk).exists():
                messages.info(request, f"You are already enrolled in {course.course_code}.")
            else:
                course.students.add(student)
                messages.success(request, f"Successfully enrolled in {course.course_code}: {course.course_name}!")
        elif request.user.is_staff or request.user.is_superuser:
            # Staff enrolling a chosen student via CourseEnrollmentForm
            form = CourseEnrollmentForm(request.POST)
            if form.is_valid():
                selected_student = form.cleaned_data['student']
                course.students.add(selected_student)
                messages.success(request, f"Student '{selected_student.name}' enrolled into {course.course_code} successfully!")
            else:
                messages.error(request, "Failed to enroll student. Please select a valid student.")
        else:
            messages.error(request, "You must be registered as a student to enroll in courses.")

    return redirect('courses:detail', pk=pk)


@login_required
def course_unenroll_view(request, pk):
    """
    Unenroll from a course.
    Demonstrates:
    - Many-to-Many ORM relation: course.students.remove(student)
    """
    course = get_object_or_404(Course, pk=pk)
    student = getattr(request.user, 'student_profile', None)

    if student and request.method == 'POST':
        if course.students.filter(pk=student.pk).exists():
            course.students.remove(student)
            messages.info(request, f"You have unenrolled from {course.course_code}.")
        else:
            messages.warning(request, "You are not enrolled in this course.")

    return redirect('courses:detail', pk=pk)

