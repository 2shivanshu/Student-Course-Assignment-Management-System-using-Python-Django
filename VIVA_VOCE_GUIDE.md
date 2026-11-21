# INT253: Django Web Development — Comprehensive Viva Voce & Practical Exam Guide

This guide is prepared for students defending the **Student Course & Assignment Management System** in their university practical examination and viva voce.

---

## Part 1: Top 20 Examination Questions & Model Answers

### Question 1: What is the architecture of Django, and how does it differ from traditional MVC?
**Answer:**  
Django follows the **MVT (Model - View - Template)** design pattern:
- **Model:** Defines the data structure and database schema via Python classes inheriting from `models.Model`. It interacts with the database via Django ORM.
- **View:** Contains the business logic. In Django, the View acts similarly to the Controller in MVC: it receives an `HttpRequest`, processes data through Models/Forms, and returns an `HttpResponse`.
- **Template:** The presentation layer containing HTML mixed with Django Template Language (DTL) tags and filters to render dynamic data.
- **In our project:** Look at `students/models.py` (Model), `students/views.py` (View), and `templates/students/student_list.html` (Template).

---

### Question 2: What is the difference between `python manage.py makemigrations` and `python manage.py migrate`?
**Answer:**  
- `makemigrations`: Inspects the `models.py` files for changes and creates human-readable Python migration blueprint files (located in `<app>/migrations/`). It does **not** modify the database itself.
- `migrate`: Reads the migration files and executes the necessary SQL DDL statements (`CREATE TABLE`, `ALTER TABLE`, `ADD COLUMN`) against the target database (`db.sqlite3`), recording applied migrations in the `django_migrations` table.
- **Bonus command:** `python manage.py sqlmigrate <app> <migration_number>` shows the exact SQL statements generated.

---

### Question 3: How does Django's CSRF protection work?
**Answer:**  
CSRF (Cross-Site Request Forgery) attacks trick an authenticated user's browser into submitting unauthorized requests to a trusted site.  
- Django protects against this using the `CsrfViewMiddleware` and the `{% csrf_token %}` template tag.
- When rendered, `{% csrf_token %}` generates a hidden input field `<input type="hidden" name="csrfmiddlewaretoken" value="...">` with a random, cryptographically signed token.
- A corresponding cookie (`csrftoken`) is stored in the browser.
- On POST/PUT/DELETE requests, the middleware compares the submitted form token against the cookie. If they do not match or are absent, Django raises a `403 Forbidden` error.
- **In our project:** Check any form template, e.g., `templates/accounts/login.html` line 16.

---

### Question 4: What is the POST-Redirect-GET (PRG) pattern, and why is it essential?
**Answer:**  
The PRG pattern prevents duplicate form submissions.  
1. **Without PRG:** A user submits a POST request (e.g., adding a course). The view renders the page directly. If the user presses F5 (refresh), the browser re-sends the POST data, creating duplicate records.
2. **With PRG:** After processing a valid POST request, the view returns a `redirect()` HTTP 302 response to a GET endpoint. When the user refreshes, they only re-request the GET page without re-submitting data.
- **In our project:** Look at `students/views.py:student_create_view` — after `form.save()`, it calls `return redirect('students:detail', pk=new_student.pk)`.

---

### Question 5: What is the difference between `forms.Form` and `forms.ModelForm`?
**Answer:**  
- `forms.Form`: A standalone form class where you explicitly declare every field (`forms.CharField`, `forms.EmailField`). You must write code to extract `form.cleaned_data` and map it to database objects manually. Example: `UserRegistrationForm` and `UserLoginForm` in `accounts/forms.py`.
- `forms.ModelForm`: A form class tied directly to a Django Model via an inner `class Meta`. It automatically generates form fields based on model definitions, inherits model validators, and provides a `.save()` method to write directly to the database. Example: `StudentForm` in `students/forms.py`.

---

### Question 6: How does Django handle form validation, and how do you write custom validation?
**Answer:**  
When `form.is_valid()` is called:
1. Field-level type validation runs (e.g., verifying an `EmailField` contains an `@` symbol).
2. Django looks for custom cleaning methods named `clean_<fieldname>()` on the form.
3. The general `clean()` method executes for multi-field cross-validation.
- **In our project:**
  - `clean_phone()` in `students/forms.py` verifies the number contains exactly 10 digits via regex `^\d{10}$`.
  - `clean_registration_number()` in `students/forms.py` ensures uniqueness while excluding the current instance during edits.
  - `clean_deadline()` in `assignments/forms.py` ensures deadlines are scheduled in the future.

---

### Question 7: How do Cookies differ from Sessions in Django?
**Answer:**  
- **Cookies:** Stored directly on the client's web browser as text strings (max 4 KB). Sent in the HTTP request headers (`request.COOKIES`) and set via response headers (`response.set_cookie()`). They can be viewed and modified by client-side tools unless marked `HttpOnly`.
- **Sessions:** Stored securely on the web server (in our SQLite `django_session` table). Only a random 32-character session identifier (`sessionid`) is stored in client cookies. The actual session dictionary data resides on the server.
- **In our project:** Visit `/accounts/session-cookie-demo/` to see both side-by-side in real time.

---

### Question 8: How does Django manage sessions, and how do you read and write session data?
**Answer:**  
Django uses `django.contrib.sessions.middleware.SessionMiddleware`. It provides a dictionary-like interface on `request.session`:
- **Write:** `request.session['visit_count'] = 5`
- **Read:** `count = request.session.get('visit_count', 0)`
- **Flush / Clear:** `request.session.flush()`
- **Set Lifetime:** `request.session.set_expiry(86400)` (in seconds) or `request.session.set_expiry(0)` (browser close).
- **In our project:** Look at `accounts/views.py:home_view` and `login_view`.

---

### Question 9: What is the `@login_required` decorator, and how does it function?
**Answer:**  
`@login_required` is an authentication decorator from `django.contrib.auth.decorators`.  
- It inspects `request.user.is_authenticated`.
- If `True`, view execution continues normally.
- If `False`, it interrupts execution and issues an HTTP 302 redirect to the URL defined by `LOGIN_URL` in `settings.py` (e.g., `/accounts/login/`), appending the original destination as a query parameter (`?next=/dashboard/`).
- **In our project:** Used in `accounts/views.py:student_dashboard_view` and `assignments/views.py:assignment_submit_view`.

---

### Question 10: What are Path Converters in Django URL routing? Give examples.
**Answer:**  
Path converters capture portions of the URL string and convert them to specific Python data types before passing them as keyword arguments to the view function:
- `<int:pk>`: Matches zero or any positive integer; converts to Python `int`.
- `<str:slug>`: Matches any non-empty string excluding `/`; converts to `str`.
- `<slug:name>`: Matches letters, numbers, hyphens, and underscores.
- **In our project:** `path('<int:pk>/', views.student_detail_view, name='detail')` in `students/urls.py`.

---

### Question 11: How do you implement Regular Expression routing in Django?
**Answer:**  
By using `re_path` from `django.urls`:
```python
from django.urls import re_path
re_path(r'^reg/(?P<reg_no>[0-9]{4,15})/$', views.student_by_reg_view, name='by_reg')
```
- `(?P<reg_no>...)` defines a named capture group that passes the matched string as `reg_no` to `student_by_reg_view(request, reg_no)`.
- **In our project:** Look at line 28 in `students/urls.py` and line 31 in `courses/urls.py`.

---

### Question 12: What is the difference between `OneToOneField`, `ForeignKey`, and `ManyToManyField`?
**Answer:**  
1. **`OneToOneField`:** A 1-to-1 relationship. Each record in Model A links to exactly one record in Model B. In our project: `Student.user` links one Student to one Django `User`.
2. **`ForeignKey`:** A 1-to-Many (1:N) relationship. Multiple records in Model A point to one record in Model B. In our project: Multiple `Assignment` objects point to one `Course`.
3. **`ManyToManyField`:** A Many-to-Many (N:M) relationship. Multiple records in Model A link to multiple records in Model B through an intermediary join table. In our project: `Course.students` allows multiple students to enroll in multiple courses.

---

### Question 13: What does `on_delete=models.CASCADE` do? What are the alternatives?
**Answer:**  
`on_delete` determines database behavior when the referenced parent object is deleted:
- `models.CASCADE`: Deletes all dependent child records automatically. (e.g., deleting a Course deletes all its Assignments and Submissions).
- `models.PROTECT`: Prevents deletion of the parent if child records exist, raising `ProtectedError`.
- `models.SET_NULL`: Sets the child's foreign key field to `NULL` (requires `null=True`).
- `models.DO_NOTHING`: Leaves the foreign key intact (can cause database integrity errors).

---

### Question 14: What is Django ORM Lazy Evaluation?
**Answer:**  
Django QuerySets are lazy. Creating a QuerySet does **not** immediately hit the database:
```python
# No database query is executed here:
students = Student.objects.filter(department='CSE')

# The database query runs only when the data is evaluated:
for s in students:   # Iteration executes the SQL query
    print(s.name)
```
Evaluation occurs on: iteration (`for`), slicing (`[:5]`), `len()`, `list()`, `bool()`, or calling `.count()`.

---

### Question 15: What is the difference between `.filter()` and `.get()` in Django ORM?
**Answer:**  
- `.filter(**kwargs)`: Returns a `QuerySet` containing zero, one, or multiple objects matching the criteria. It never raises an exception if nothing matches.
- `.get(**kwargs)`: Returns exactly **one** model instance. It raises `Model.DoesNotExist` if no object is found, and `Model.MultipleObjectsReturned` if more than one object matches.

---

### Question 16: What is `get_object_or_404()`?
**Answer:**  
It is a Django shortcut function (`django.shortcuts.get_object_or_404`). It attempts to call `.get()` on a model or QuerySet. If `DoesNotExist` is raised, instead of crashing with an uncaught 500 error, it catches the exception and raises `django.http.Http404`, rendering the custom 404 error page.  
- **In our project:** Used in `students/views.py:student_detail_view` and `courses/views.py:course_detail_view`.

---

### Question 17: How do you handle file uploads in Django forms?
**Answer:**  
Two mandatory requirements:
1. In the HTML form: Add `enctype="multipart/form-data"` and `method="POST"`.
2. In the Django view: Pass both `request.POST` and `request.FILES` to the form instance:
   ```python
   form = AssignmentSubmissionForm(request.POST, request.FILES)
   ```
3. In `settings.py`: Configure `MEDIA_URL` and `MEDIA_ROOT`.
- **In our project:** Look at `assignments/views.py:assignment_submit_view` and `templates/assignments/submission_form.html`.

---

### Question 18: What is a Django Context Processor?
**Answer:**  
A Python function that accepts `request` and returns a dictionary. Django merges this dictionary into the template context of **every** template rendered with `RequestContext`.  
- It avoids repeating common data (such as user information, theme preferences, or visit counts) in every individual view.
- **In our project:** Look at `accounts/context_processors.py:global_user_context`.

---

### Question 19: How do you customize the Django Admin site?
**Answer:**  
By subclassing `admin.ModelAdmin` and registering it using `@admin.register(ModelName)`:
- `list_display`: Tuple of model fields to display as table columns.
- `list_filter`: Sidebar filters for quick querying.
- `search_fields`: Search bar querying specified fields.
- `ordering`: Default sort order.
- `fieldsets`: Organizing the detail/edit form into logical sections.
- `filter_horizontal`: Dual-pane selector for `ManyToManyField`.
- **In our project:** Look at `courses/admin.py` and `students/admin.py`.

---

### Question 20: How do you write and run automated tests in Django?
**Answer:**  
By creating test classes inheriting from `django.test.TestCase` in `tests.py`.  
- Django creates a temporary test database, runs the test methods (prefixed with `test_`), asserts conditions using `self.assertEqual()`, `self.assertContains()`, `self.assertTrue()`, and destroys the test database afterwards.
- Run with: `python manage.py test`.
- **In our project:** 24 unit and integration tests are implemented across all 4 apps.

---

## Part 2: Step-by-Step Live Demonstration Script for Faculty

When presenting to your faculty, follow this structured demonstration:

```
Step 1: System Overview & Landing Page
        -> Open http://127.0.0.1:8000/
        -> Point out the navbar, stats cards, and INT253 syllabus cards.
        -> Point out the session visit counter: "Visits: 1".

Step 2: Server-Side Validation Test (Unit 4)
        -> Click "Register Student".
        -> Intentionally enter a 3-digit phone number: "123".
        -> Click "Complete Registration".
        -> Show the inline Bootstrap error: "Phone number must contain exactly 10 numeric digits."

Step 3: Student Login & Dashboard (Unit 6)
        -> Navigate to Login.
        -> Enter credentials: student1 / pass123.
        -> Land on Student Dashboard.
        -> Point out Aarav Sharma's details, enrolled courses, and pending tasks.

Step 4: Course Enrollment & Many-to-Many ORM (Unit 5)
        -> Click "Courses" in the navigation bar.
        -> Locate "Cloud Computing and Web Services (INT306)".
        -> Click "Enroll".
        -> Show the success notification and the "Enrolled" badge.

Step 5: Assignment Submission with File Attachment (Unit 4 & 5)
        -> Click "Assignments".
        -> Select "Lab 1: Django Architecture & Function-Based Views".
        -> Click "Submit Solution".
        -> Enter code notes, optionally attach a file, and click "Confirm Submission".
        -> Show that status updates to "Submitted On Time".

Step 6: Path Converter vs Regex Routing Demonstration (Unit 2)
        -> In the address bar, type: http://127.0.0.1:8000/courses/1/ (Path Converter <int:pk>)
        -> In the address bar, type: http://127.0.0.1:8000/courses/code/INT253/ (Regex re_path)
        -> Explain that both routes resolve to the exact same course view.

Step 7: Unit 6 Interactive Cookie & Session Lab (Unit 6)
        -> Click "Unit 6 Lab (Cookies & Sessions)".
        -> Click "Increment Counter (+1)" to demonstrate request.session mutation.
        -> Select "Dark Slate Theme" and click "Set HTTP Cookie" to show client-side theme switching.
        -> Add a custom cookie: key="subject", value="Django". Show it under browser cookies.

Step 8: Faculty Admin Console & Grading Workflow (Unit 6 & 4)
        -> Log out and log in as: admin / admin123.
        -> Redirects automatically to the Faculty Console (/admin-dashboard/).
        -> Locate Aarav Sharma's submission under "Submissions Awaiting Evaluation".
        -> Click "Grade Now".
        -> Award 96 marks, select status "Graded", type constructive remarks, and submit.
        -> Show that pending tasks counter decreases by 1.

Step 9: Django Admin Site Customization (Unit 5)
        -> Click "Django Admin" or open http://127.0.0.1:8000/admin/.
        -> Show Courses: demonstrate the filter_horizontal widget for student enrollment.
        -> Show Students: demonstrate list_filter, search_fields, and fieldsets.

Step 10: Terminal Proof & Automated Tests (Unit 3 & 5)
        -> Open PowerShell.
        -> Run: python manage.py test
        -> Show that all 24 tests pass with "OK".
        -> Run: python shell_demo.py
        -> Walk through the ORM queries executing in the terminal.
```

