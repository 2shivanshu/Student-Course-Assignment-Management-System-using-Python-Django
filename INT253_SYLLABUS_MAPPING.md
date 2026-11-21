# INT253 – Web Development in Python Using Django
## University Course Syllabus Mapping & Practical Demonstration Guide

This document maps every topic covered in **INT253 (Units I – VI)** directly to its working implementation in the **Student Course & Assignment Management System**. Use this reference during practical evaluations, lab assessments, and external viva examinations.

---

## Unit I: Introduction to Web Development & Django

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **1.1 Web Fundamentals & MVT Architecture** | Request-Response cycle, stateless HTTP, separation of Model, View, and Template. | The entire application follows Django's Model-View-Template pattern. Models define SQLite tables, Views handle logic, and Templates display presentation. | `student_management/settings.py`<br>`student_management/urls.py` |
| **1.2 Virtual Environment & Pip** | Environment isolation and package dependency management. | Standard virtual environment setup using `requirements.txt`. | `requirements.txt` |
| **1.3 Django Project & Multi-App Setup** | `django-admin startproject` and `python manage.py startapp`. Dividing features into decoupled modular applications. | Project `student_management` configured with 4 custom apps: `accounts`, `students`, `courses`, `assignments`. | `student_management/settings.py`<br>(lines 39-44 `INSTALLED_APPS`) |
| **1.4 Project Configuration (`settings.py`)** | `BASE_DIR`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `MIDDLEWARE`, `TEMPLATES`, `STATICFILES_DIRS`. | Complete, clean settings file with custom context processors, session age, and message tags. | `student_management/settings.py` |
| **1.5 Database Configuration** | SQLite3 connection engine, database location path. | Configured with `'ENGINE': 'django.db.backends.sqlite3'` pointing to `BASE_DIR / 'db.sqlite3'`. | `student_management/settings.py` (lines 75-81) |
| **1.6 Core `manage.py` Commands** | Administrative tasks: `runserver`, `makemigrations`, `migrate`, `createsuperuser`, `test`, `shell`, `check`. | All commands tested and documented. Includes automated seed script and test suite. | `manage.py`<br>`seed_demo_data.py`<br>`shell_demo.py` |

---

## Unit II: Django Views and URL Routing

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **2.1 Function-Based Views (FBVs)** | Writing view functions accepting `HttpRequest` and returning `HttpResponse`. | 100% pure function-based views implemented across all 4 apps. No class-based views or REST framework. | `accounts/views.py`<br>`students/views.py`<br>`courses/views.py`<br>`assignments/views.py` |
| **2.2 `HttpRequest` & `HttpResponse` Objects** | Examining `request.method`, `request.GET`, `request.POST`, `request.FILES`, `request.session`, `request.COOKIES`. | Views parse HTTP methods, read query parameters, handle file uploads, and return `render()` or `redirect()`. | `accounts/views.py:home_view`<br>`courses/views.py:course_list_view` |
| **2.3 URL Routing & `include()`** | Project-level routing delegating to application-level `urls.py` using `include()` with app namespaces. | Project `student_management/urls.py` delegates to `accounts.urls`, `students.urls`, `courses.urls`, and `assignments.urls`. | `student_management/urls.py` (lines 20-33) |
| **2.4 Path Converters (`<int:pk>`)** | Type-safe URL parameter capture converting string parameters to Python data types. | Used throughout for object detail, editing, deleting, and submitting: `<int:pk>/`. | `students/urls.py:path('<int:pk>/', ...)`<br>`courses/urls.py:path('<int:pk>/', ...)` |
| **2.5 Regular Expression Routing (`re_path`)** | Pattern-based URL matching using regex named groups `(?P<name>pattern)`. | 1. Student lookup by numeric registration number: `r'^reg/(?P<reg_no>[0-9]{4,15})/$'`<br>2. Course lookup by uppercase code: `r'^code/(?P<course_code>[A-Za-z0-9]{3,10})/$'` | `students/urls.py` (line 28)<br>`courses/urls.py` (line 31) |
| **2.6 Error Handling (`404` and `500`)** | `get_object_or_404`, custom error handlers (`handler404`, `handler500`), returning `status=404`. | Custom `custom_404_view` and `custom_500_view` hooked to `handler404` and `handler500` rendering branded templates. | `student_management/urls.py` (lines 35-37)<br>`accounts/views.py:custom_404_view`<br>`templates/404.html` |

---

## Unit III: Django Template System (DTL)

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **3.1 Template Inheritance** | DRY principle using `{% extends %}` and `{% block %}` to maintain uniform layout. | Master `templates/base.html` defines navbar, sidebar, alert messages, and footer. All child pages inherit from it. | `templates/base.html`<br>`templates/home.html` |
| **3.2 DTL Variables & Tags** | Double curly braces `{{ var }}` and logic tags `{% if %}`, `{% elif %}`, `{% else %}`, `{% for %}`, `{% empty %}`. | Used extensively for conditional student enrollment banners, due deadline warnings, loops over students and courses. | `templates/dashboard/student_dashboard.html`<br>`templates/courses/course_list.html` |
| **3.3 DTL Filters** | Transforming output formatting using pipeline `\|`. | Demonstrated: `\|truncatewords:20`, `\|date:"M d, Y H:i"`, `\|default:"light"`, `\|length`, `\|upper`. | `templates/home.html` (lines 148, 168)<br>`templates/base.html` (line 19) |
| **3.4 Static Files Configuration** | Managing CSS, JavaScript, and static images with `{% load static %}`. | Configured `static/css/custom.css` and `static/js/custom.js` with responsive themes and styling. | `student_management/settings.py` (lines 98-100)<br>`static/css/custom.css` |
| **3.5 Custom Context Processor** | Making variables available across all templates automatically without view duplication. | `accounts.context_processors.global_user_context` supplies `current_student`, `theme_preference`, and `session_visit_count` to every page. | `accounts/context_processors.py`<br>`student_management/settings.py` (line 62) |
| **3.6 Template Debugging & Django Tests** | Unit testing view responses, template usage, and context assertions. | 24 automated unit tests verifying template loading, context dictionaries, and response codes. | `accounts/tests.py`<br>`students/tests.py` |

---

## Unit IV: Django Forms and Form Processing

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **4.1 Django `forms.Form`** | Standard form class with field definitions, widgets, and validation. | `UserRegistrationForm` and `UserLoginForm` defined with custom fields and password verification. | `accounts/forms.py` |
| **4.2 Django `forms.ModelForm`** | Automatically generating form fields and saving directly to database models. | `StudentForm`, `CourseForm`, `AssignmentForm`, `AssignmentSubmissionForm`, and `SubmissionGradingForm`. | `students/forms.py`<br>`courses/forms.py`<br>`assignments/forms.py` |
| **4.3 CSRF Protection** | Securing form POST submissions against cross-site request forgery via `{% csrf_token %}`. | Every POST form in the application contains the `{% csrf_token %}` directive. | All template form elements (e.g. `templates/accounts/login.html`) |
| **4.4 Server-Side Form Validation** | Field cleaning with `clean_<field>()` and cross-field cleaning with `clean()`. | 1. Phone number format validation (exactly 10 digits).<br>2. Unique registration number checks.<br>3. Deadline must be in future.<br>4. Max marks boundary verification. | `accounts/forms.py:clean_phone`<br>`students/forms.py:clean_registration_number`<br>`assignments/forms.py:clean_deadline` |
| **4.5 Rendering Form Errors** | Visualizing invalid fields using Bootstrap feedback classes. | All form templates explicitly loop over `form.non_field_errors` and field-level `form.<field>.errors`. | `templates/accounts/register.html`<br>`templates/assignments/submission_form.html` |
| **4.6 POST-Redirect-GET (PRG) Pattern** | Preventing duplicate form submissions when users refresh the browser. | Views process POST, call `form.save()`, set `messages.success()`, and return `redirect('...')`. | `accounts/views.py:register_view`<br>`assignments/views.py:assignment_submit_view` |
| **4.7 File Upload Handling** | Multipart form submissions using `enctype="multipart/form-data"` and `request.FILES`. | Students can upload assignment solution scripts/documents saved to the `media/` directory. | `assignments/views.py:assignment_submit_view`<br>`templates/assignments/submission_form.html` |

---

## Unit V: Models, ORM, and Django Administration

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **5.1 Database Models & Field Types** | Defining schema in Python classes using `models.CharField`, `EmailField`, `DateField`, `DateTimeField`, `TextField`, `IntegerField`. | All 4 required models implemented: `Student`, `Course`, `Assignment`, `Submission`. | `students/models.py`<br>`courses/models.py`<br>`assignments/models.py` |
| **5.2 Relationships & Cardinality** | 1. `OneToOneField`: User to Student.<br>2. `ForeignKey`: Assignment to Course; Submission to Student/Assignment.<br>3. `ManyToManyField`: Course to Student. | Complete relational network with `on_delete=models.CASCADE` and reverse related names (`related_name`). | `students/models.py:Student.user`<br>`courses/models.py:Course.students`<br>`assignments/models.py:Submission` |
| **5.3 Migrations Management** | Two-step database schema versioning: `makemigrations` and `migrate`. | Migration files generated in each app; initial schema cleanly deployed to SQLite database. | `<app>/migrations/0001_initial.py` |
| **5.4 Django ORM & QuerySet API** | Data retrieval without writing raw SQL queries. | Demonstrated in views and shell demo:<br>- `.all()`: Retrieve all records<br>- `.filter(Q(...) | Q(...))`: Complex search<br>- `.get(id=...)`: Single object retrieval<br>- `.exclude()`: Pending assignments<br>- `.annotate(student_count=Count('students'))`<br>- `.aggregate(Avg('marks_obtained'))` | `courses/views.py:course_list_view`<br>`accounts/views.py:student_dashboard_view`<br>`shell_demo.py` |
| **5.5 Interactive Django Shell** | Executing interactive ORM commands using `python manage.py shell`. | Standalone demonstration script `shell_demo.py` demonstrating CRUD operations and relational lookups. | `shell_demo.py` |
| **5.6 Django Admin Site Customization** | Registering models and creating custom `ModelAdmin` interfaces. | Custom ModelAdmin classes for all models configuring:<br>- `list_display`: Multi-column tables<br>- `list_filter`: Sidebar filtering<br>- `search_fields`: Search boxes<br>- `ordering`: Sorting defaults<br>- `fieldsets`: Logical collapsible sections<br>- `filter_horizontal`: For ManyToMany student enrollment | `students/admin.py`<br>`courses/admin.py`<br>`assignments/admin.py` |

---

## Unit VI: Cookies, Sessions, and User Authentication

| Syllabus Topic | Concepts & Theory | Working Implementation in Project | File & Function Reference |
|---|---|---|---|
| **6.1 HTTP State Management & Cookies** | Stateless protocol, client-side cookie storage, cookie lifetime (`max_age`), setting and deleting cookies. | 1. `response.set_cookie('theme_preference', theme)`<br>2. `request.COOKIES.get('theme_preference')`<br>3. `response.set_cookie('last_viewed_course', code)`<br>4. `response.delete_cookie(...)` | `accounts/views.py:session_cookie_demo_view`<br>`courses/views.py:course_detail_view`<br>`templates/accounts/session_cookie_demo.html` |
| **6.2 Django Session Framework** | Server-side state stored in `django_session` table referenced by 32-character `sessionid` cookie. | 1. Page visit tracking: `request.session['visit_count'] = count`<br>2. Welcome message and login timestamps: `request.session['last_login_time']`<br>3. Session expiry control: `request.session.set_expiry(0)` vs `request.session.set_expiry(1209600)` | `accounts/views.py:home_view`<br>`accounts/views.py:login_view`<br>`accounts/views.py:session_cookie_demo_view` |
| **6.3 Built-in User Authentication** | Verifying user identities and managing login states. | Full authentication cycle implemented:<br>- `authenticate(username, password)`: Hash verification<br>- `login(request, user)`: Attaching user to session<br>- `logout(request)`: Terminating session | `accounts/views.py:login_view`<br>`accounts/views.py:logout_view` |
| **6.4 Authorization & Access Control** | Protecting views from unauthenticated access and enforcing role separation. | 1. `@login_required`: Restricts student and faculty pages.<br>2. Role separation: `user.is_staff` or `user.is_superuser` gates the Faculty Console and grading views.<br>3. `current_student` limits submissions to enrolled courses. | `accounts/views.py:student_dashboard_view`<br>`accounts/views.py:admin_dashboard_view`<br>`assignments/views.py:submission_grade_view` |
| **6.5 Interactive Unit 6 Demonstration Lab** | Dedicated laboratory environment for viva examiners to inspect live sessions and browser cookies. | Dedicated route `/accounts/session-cookie-demo/` with live session key display, session counter manipulation (+1 and Reset), theme cookie selector, custom key-value cookie setter, and cookie wipe button. | `accounts/views.py:session_cookie_demo_view`<br>`templates/accounts/session_cookie_demo.html` |

---

## Summary Table for Practical Viva Examination

When the faculty examiner asks you to demonstrate specific syllabus topics, use this quick navigation table:

| Examiner Question / Topic | What to Click / Run | Expected Result on Screen |
|---|---|---|
| **"Show me your database relationships."** | Run `python shell_demo.py` or open `http://127.0.0.1:8000/admin/`. | Shows `OneToOneField`, `ForeignKey`, and `ManyToManyField` relationships in terminal and Admin console. |
| **"Demonstrate URL path converters and regular expressions."** | Visit `/courses/1/` (path converter) and `/courses/code/INT253/` (regex route). | Both routes resolve to the exact same course syllabus page cleanly. |
| **"Show me server-side form validation."** | Go to `/accounts/register/` and enter a 3-digit phone or mismatching passwords. | Form displays inline Bootstrap validation errors and prevents database insertion. |
| **"Demonstrate client-side Cookies and server-side Sessions."** | Open `/accounts/session-cookie-demo/`. | Click "+1 Counter" to increment session. Switch theme to "Dark Slate" or "Blue" to demonstrate cookie storage. |
| **"Show me student submission and faculty grading workflow."** | 1. Login as `student1` (`pass123`) & submit assignment.<br>2. Login as `admin` (`admin123`) & grade it on the Admin Dashboard. | Real-time status changes from "Pending" to "Graded" with awarded marks and feedback. |
| **"Run your project test suite."** | Execute `python manage.py test`. | All 24 automated unit tests pass with `OK`. |

