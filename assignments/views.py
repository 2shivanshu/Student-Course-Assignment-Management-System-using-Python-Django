"""
Function-Based Views for Assignments and Submissions App.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs - FBVs, Path Converters, Request Methods
Unit 4: Forms - File uploads, Server-side validations, PRG pattern
Unit 5: Models & ORM - ForeignKey filters and queries
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Assignment, Submission
from .forms import AssignmentForm, AssignmentSubmissionForm, SubmissionGradingForm
from courses.models import Course


def assignment_list_view(request):
    """
    List all assignments across courses.
    Demonstrates:
    - Filtering by Course and Deadline status (Active vs Past Due)
    - Distinguishing student submission statuses
    """
    course_id = request.GET.get('course')
    filter_status = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '').strip()

    assignments = Assignment.objects.select_related('course').all()

    if course_id:
        assignments = assignments.filter(course_id=course_id)

    if search_query:
        assignments = assignments.filter(
            Q(assignment_title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(course__course_code__icontains=search_query)
        )

    now = timezone.now()
    if filter_status == 'active':
        assignments = assignments.filter(deadline__gte=now)
    elif filter_status == 'past':
        assignments = assignments.filter(deadline__lt=now)

    courses = Course.objects.all().order_by('course_code')

    # If user is a student, collect which assignments they have already submitted
    submitted_assignment_ids = set()
    my_submissions_map = {}
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        subs = Submission.objects.filter(student=request.user.student_profile)
        for s in subs:
            submitted_assignment_ids.add(s.assignment_id)
            my_submissions_map[s.assignment_id] = s

    context = {
        'assignments': assignments,
        'total_count': assignments.count(),
        'courses': courses,
        'selected_course': int(course_id) if course_id and course_id.isdigit() else None,
        'filter_status': filter_status,
        'search_query': search_query,
        'submitted_assignment_ids': submitted_assignment_ids,
        'my_submissions_map': my_submissions_map,
        'page_title': 'Course Assignments Portal',
    }
    return render(request, 'assignments/assignment_list.html', context)


def assignment_detail_view(request, pk):
    """
    Display single assignment instructions, deadline countdown, and submissions.
    Demonstrates:
    - Path converter <int:pk>
    - Conditional views based on user role (student vs staff)
    - Showing student's own submission or all submissions for staff
    """
    assignment = get_object_or_404(Assignment.objects.select_related('course'), pk=pk)

    # Submission for current logged in student (if any)
    my_submission = None
    is_enrolled = False

    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        is_enrolled = assignment.course.students.filter(pk=student.pk).exists()
        my_submission = Submission.objects.filter(assignment=assignment, student=student).first()

    # Submissions received (for faculty/staff inspection)
    all_submissions = []
    if request.user.is_staff or request.user.is_superuser:
        all_submissions = assignment.submissions.select_related('student').all()

    context = {
        'assignment': assignment,
        'my_submission': my_submission,
        'is_enrolled': is_enrolled,
        'all_submissions': all_submissions,
        'is_past_due': assignment.is_past_due,
        'page_title': f"Assignment: {assignment.assignment_title}",
    }
    return render(request, 'assignments/assignment_detail.html', context)


@login_required
def assignment_create_view(request):
    """
    Create a new assignment for a course (Faculty / Administrator).
    Demonstrates:
    - ModelForm creation
    - Server-side deadline validation
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only faculty can post new assignments.")
        return redirect('assignments:list')

    course_id = request.GET.get('course')
    initial_data = {}
    if course_id:
        initial_data['course'] = course_id

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save()
            messages.success(request, f"Assignment '{new_assignment.assignment_title}' published successfully!")
            return redirect('assignments:detail', pk=new_assignment.pk)
        else:
            messages.error(request, "Please fix the errors in the assignment form.")
    else:
        form = AssignmentForm(initial=initial_data)

    context = {
        'form': form,
        'is_edit': False,
        'page_title': 'Create New Assignment',
    }
    return render(request, 'assignments/assignment_form.html', context)


@login_required
def assignment_update_view(request, pk):
    """
    Update an existing assignment (Faculty / Administrator).
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only faculty can modify assignments.")
        return redirect('assignments:detail', pk=pk)

    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Assignment '{assignment.assignment_title}' updated successfully.")
            return redirect('assignments:detail', pk=assignment.pk)
        else:
            messages.error(request, "Please check the submitted form values.")
    else:
        form = AssignmentForm(instance=assignment)

    context = {
        'form': form,
        'assignment': assignment,
        'is_edit': True,
        'page_title': f"Edit Assignment: {assignment.assignment_title}",
    }
    return render(request, 'assignments/assignment_form.html', context)


@login_required
def assignment_delete_view(request, pk):
    """
    Delete an assignment (Faculty / Administrator).
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only administrators can delete assignments.")
        return redirect('assignments:detail', pk=pk)

    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == 'POST':
        title = assignment.assignment_title
        assignment.delete()
        messages.success(request, f"Assignment '{title}' was permanently deleted.")
        return redirect('assignments:list')

    context = {
        'assignment': assignment,
        'page_title': f"Confirm Deletion: {assignment.assignment_title}",
    }
    return render(request, 'assignments/assignment_confirm_delete.html', context)


@login_required
def assignment_submit_view(request, pk):
    """
    Submit work for an assignment.
    Demonstrates:
    - File upload handling with request.FILES
    - Checking if student is enrolled in the course
    - Auto-marking 'Late' if past deadline
    - Creating or updating Submission record
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    student = getattr(request.user, 'student_profile', None)

    if not student:
        messages.error(request, "Only registered students can submit assignments.")
        return redirect('assignments:detail', pk=pk)

    # Ensure student is enrolled in course
    if not assignment.course.students.filter(pk=student.pk).exists():
        messages.warning(request, f"You must enroll in '{assignment.course.course_code}' before submitting assignments.")
        return redirect('courses:detail', pk=assignment.course.pk)

    # Check for existing submission
    existing_submission = Submission.objects.filter(assignment=assignment, student=student).first()

    if request.method == 'POST':
        # File handling requires both request.POST and request.FILES
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.assignment = assignment

            # Check deadline status
            if timezone.now() > assignment.deadline:
                submission.status = 'Late'
                messages.warning(request, "Your submission was recorded after the official deadline (Marked Late).")
            else:
                submission.status = 'Submitted'
                messages.success(request, "Assignment submitted successfully on time!")

            submission.save()
            return redirect('assignments:detail', pk=assignment.pk)
        else:
            messages.error(request, "Please check the submission form errors below.")
    else:
        form = AssignmentSubmissionForm(instance=existing_submission)

    context = {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission,
        'page_title': f"Submit: {assignment.assignment_title}",
    }
    return render(request, 'assignments/submission_form.html', context)


@login_required
def submission_grade_view(request, pk):
    """
    Grade a student submission (Faculty / Staff).
    Demonstrates:
    - ModelForm for grading and feedback
    - Updating submission status to 'Graded'
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Permission denied: Only faculty can grade student submissions.")
        return redirect('assignments:list')

    submission = get_object_or_404(
        Submission.objects.select_related('student', 'assignment', 'assignment__course'),
        pk=pk
    )

    if request.method == 'POST':
        form = SubmissionGradingForm(request.POST, instance=submission)
        if form.is_valid():
            graded_sub = form.save(commit=False)
            graded_sub.status = 'Graded'
            graded_sub.save()
            messages.success(
                request,
                f"Graded submission for {submission.student.name} ({graded_sub.marks_obtained}/{submission.assignment.max_marks} marks)!"
            )
            return redirect('assignments:detail', pk=submission.assignment.pk)
        else:
            messages.error(request, "Please check the grading inputs.")
    else:
        form = SubmissionGradingForm(instance=submission, initial={'status': 'Graded'})

    context = {
        'form': form,
        'submission': submission,
        'assignment': submission.assignment,
        'student': submission.student,
        'page_title': f"Grade Submission: {submission.student.name}",
    }
    return render(request, 'assignments/submission_grade.html', context)

