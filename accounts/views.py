"""
Views for Accounts, Authentication, Dashboard, and Cookie/Session Demonstrations.

INT253: Web Development in Python Using Django
Unit 2: Views and URLs (FBVs, HttpRequest, HttpResponse, render)
Unit 6: Cookies, Sessions, and Django Built-in Authentication
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg

from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm, CookieDemoForm
from students.models import Student
from courses.models import Course
from assignments.models import Assignment, Submission


def home_view(request):
    """
    Public Landing Page.
    Demonstrates:
    - Function-based view (FBV)
    - HttpRequest inspection
    - Passing dynamic context dictionary to render()
    - ORM aggregates (.count())
    """
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    featured_courses = Course.objects.all()[:3]

    # Session visit counter demonstration (Unit 6)
    visits = request.session.get('visit_count', 0) + 1
    request.session['visit_count'] = visits

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'featured_courses': featured_courses,
        'page_title': 'Welcome to Student Management Portal',
    }
    return render(request, 'home.html', context)


def register_view(request):
    """
    User and Student Profile Registration View.
    Demonstrates:
    - GET request (rendering empty form)
    - POST request (binding data, validation, creating records)
    - CSRF verification in forms
    - Server-side validation via clean methods
    - POST-Redirect-GET (PRG) pattern with messages framework
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            reg_num = form.cleaned_data['registration_number']
            phone = form.cleaned_data['phone']
            department = form.cleaned_data['department']

            # 1. Create User in auth_user table
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 2. Create linked Student Profile in students table
            student = Student.objects.create(
                user=user,
                name=name,
                email=email,
                phone=phone,
                registration_number=reg_num,
                department=department,
                join_date=timezone.now().date()
            )

            messages.success(request, f"Registration successful for {name}! You can now log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        # GET request: Instantiate empty form
        form = UserRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Student Registration'
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """
    User Login View using Django Authentication Framework.
    Demonstrates:
    - authenticate() verifying credentials against hash
    - login() creating user session in django_session table
    - Managing session cookies (remember_me setting session expiry)
    - Role-based redirection (Admin/Staff vs Student)
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me')

            # Authenticate credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Manage session lifetime based on 'Remember Me'
                    if not remember_me:
                        # Session expires when user closes the browser
                        request.session.set_expiry(0)
                    else:
                        # Session expires after 2 weeks (1209600 seconds)
                        request.session.set_expiry(1209600)

                    # Unit 6: Store session-based welcome message and login timestamp
                    request.session['last_login_time'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                    messages.success(request, f"Welcome back, {user.username}! Login successful.")

                    # Role-based redirect
                    if user.is_staff or user.is_superuser:
                        return redirect('admin_dashboard')
                    return redirect('dashboard')
                else:
                    messages.error(request, "This account is inactive. Please contact administrator.")
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'page_title': 'Portal Login'
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    """
    User Logout View.
    Demonstrates:
    - logout(request) flushes the current session
    - Redirecting to landing page with flash message
    """
    logout(request)
    messages.info(request, "You have been securely logged out. Have a productive day!")
    return redirect('home')


@login_required
def profile_view(request):
    """
    User Profile View & Update.
    Demonstrates:
    - @login_required decorator protecting the view
    - OneToOne reverse relationship (request.user.student_profile)
    - ModelForm instance updates
    """
    student = getattr(request.user, 'student_profile', None)

    if request.method == 'POST':
        if student:
            form = UserProfileUpdateForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Your student profile has been updated successfully!")
                return redirect('accounts:profile')
        else:
            messages.error(request, "Staff profile editing is managed via the admin console.")
            return redirect('accounts:profile')
    else:
        form = UserProfileUpdateForm(instance=student) if student else None

    context = {
        'student': student,
        'form': form,
        'page_title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def student_dashboard_view(request):
    """
    Interactive Student Dashboard.
    Demonstrates:
    - Querying related models through ORM: student.enrolled_courses, student.submissions
    - Computing metrics: pending assignments, completed submissions, average grade
    - Session tracking display
    """
    # If a staff member lands here, they can view or jump to admin dashboard
    student = getattr(request.user, 'student_profile', None)

    if not student:
        # If logged in as superuser/staff without student profile
        messages.info(request, "You are logged in as an Administrator/Faculty member.")
        return redirect('admin_dashboard')

    # Enrolled courses
    enrolled_courses = student.enrolled_courses.all()

    # Submissions made by this student
    my_submissions = student.submissions.select_related('assignment', 'assignment__course').all()

    # IDs of assignments already submitted
    submitted_assignment_ids = my_submissions.values_list('assignment_id', flat=True)

    # Pending assignments from enrolled courses that haven't been submitted yet
    pending_assignments = Assignment.objects.filter(
        course__in=enrolled_courses
    ).exclude(
        id__in=submitted_assignment_ids
    ).order_by('deadline')

    # Completed submissions
    graded_submissions = my_submissions.filter(status='Graded')
    avg_marks = graded_submissions.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'enrolled_count': enrolled_courses.count(),
        'pending_assignments': pending_assignments,
        'pending_count': pending_assignments.count(),
        'my_submissions': my_submissions[:5],
        'total_submissions': my_submissions.count(),
        'avg_marks': round(avg_marks, 1),
        'last_login_time': request.session.get('last_login_time', 'First session'),
        'page_title': 'Student Dashboard',
    }
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    """
    Comprehensive Admin / Faculty Management Dashboard.
    Demonstrates:
    - Permission checking (request.user.is_staff or is_superuser)
    - Complex ORM queries: pending submissions to grade, department statistics
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.warning(request, "Access restricted. You must be faculty or administrator to access the Admin Dashboard.")
        return redirect('dashboard')

    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()

    # Submissions awaiting evaluation
    pending_grading = Submission.objects.filter(status__in=['Submitted', 'Late']).select_related('student', 'assignment', 'assignment__course')[:10]

    # Recent student signups
    recent_students = Student.objects.all().order_by('-created_at')[:5]

    # Courses with student counts
    popular_courses = Course.objects.annotate(enrollment_count=Count('students')).order_by('-enrollment_count')[:5]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'pending_grading': pending_grading,
        'pending_grading_count': Submission.objects.filter(status__in=['Submitted', 'Late']).count(),
        'recent_students': recent_students,
        'popular_courses': popular_courses,
        'page_title': 'Faculty & Admin Console',
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


def session_cookie_demo_view(request):
    """
    Dedicated Interactive Lab for INT253 Unit 6: Cookies and Sessions.
    Demonstrates:
    1. Reading and writing server-side sessions via request.session
    2. Session methods: .get(), .keys(), .flush(), .set_expiry()
    3. Reading client-side cookies via request.COOKIES.get()
    4. Setting client-side cookies via HttpResponse.set_cookie()
    5. Deleting client-side cookies via HttpResponse.delete_cookie()
    """
    # 1. Session Operations
    action = request.POST.get('action') or request.GET.get('action')

    # Default response template rendering
    form = CookieDemoForm(initial={'theme': request.COOKIES.get('theme_preference', 'light')})

    # Read all current session items for inspection
    session_data = {k: request.session.get(k) for k in request.session.keys()}

    # Read all client cookies
    cookies_data = dict(request.COOKIES)

    response = render(request, 'accounts/session_cookie_demo.html', {
        'form': form,
        'session_data': session_data,
        'cookies_data': cookies_data,
        'current_theme': request.COOKIES.get('theme_preference', 'light'),
        'session_visit_count': request.session.get('visit_count', 0),
        'session_key': request.session.session_key,
        'page_title': 'Unit 6: Cookies & Session Demonstration Lab',
    })

    if request.method == 'POST':
        if action == 'increment_session':
            count = request.session.get('lab_counter', 0) + 1
            request.session['lab_counter'] = count
            messages.success(request, f"Session counter incremented to {count}!")
            return redirect('accounts:session_cookie_demo')

        elif action == 'reset_session_counter':
            request.session['lab_counter'] = 0
            messages.info(request, "Session counter reset to 0.")
            return redirect('accounts:session_cookie_demo')

        elif action == 'set_cookie':
            form = CookieDemoForm(request.POST)
            if form.is_valid():
                selected_theme = form.cleaned_data['theme']
                custom_key = form.cleaned_data['custom_key']
                custom_val = form.cleaned_data['custom_value']

                # Create redirect response and attach cookies
                res = redirect('accounts:session_cookie_demo')
                # Set theme cookie (expires in 7 days = 604800 seconds)
                res.set_cookie('theme_preference', selected_theme, max_age=604800)

                if custom_key and custom_val:
                    # Sanitize key name for cookie specification
                    safe_key = "".join(c for c in custom_key if c.isalnum() or c in '_-')
                    res.set_cookie(safe_key, custom_val, max_age=3600)
                    messages.success(request, f"Custom cookie '{safe_key}' and Theme '{selected_theme}' saved successfully!")
                else:
                    messages.success(request, f"Theme preference updated to '{selected_theme}' via HTTP Cookie!")
                return res

        elif action == 'clear_cookies':
            res = redirect('accounts:session_cookie_demo')
            # Delete theme cookie and custom cookies
            res.delete_cookie('theme_preference')
            for key in request.COOKIES:
                if key not in ['sessionid', 'csrftoken']:
                    res.delete_cookie(key)
            messages.info(request, "All demonstration cookies have been removed from your browser.")
            return res

    return response


def custom_404_view(request, exception=None):
    """
    Custom 404 Not Found View.
    Demonstrates INT253 Unit 2 error handling with friendly message.
    """
    context = {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': 'The page or resource you requested could not be located on the server.',
        'page_title': '404 - Page Not Found'
    }
    return render(request, '404.html', context, status=404)


def custom_500_view(request):
    """
    Custom 500 Internal Server Error View.
    """
    context = {
        'error_code': '500',
        'error_title': 'Internal Server Error',
        'error_message': 'An unexpected server error occurred. Our team has been notified.',
        'page_title': '500 - Server Error'
    }
    return render(request, '500.html', context, status=500)

