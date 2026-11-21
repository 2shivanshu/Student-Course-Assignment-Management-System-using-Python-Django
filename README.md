# Student Course & Assignment Management System

A production-quality, full-featured web application built with **Python 3** and **Django** framework, engineered specifically for university examination and practical demonstration for:

**Course:** INT253 – Web Development in Python Using Django  
**Architecture:** Django MVT (Model - View - Template)  
**Database:** SQLite3 Relational Database  
**Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons  

---

## 1. Project Introduction

The **Student Course & Assignment Management System** is an educational management portal designed to streamline academic interactions between university students and faculty members. 

It covers the complete academic workflow:
- **Students** can create accounts, view available course catalogs, enroll in courses, access assignment problem statements, submit solutions (text and file uploads), track deadlines, and view instructor grades and qualitative feedback.
- **Faculty / Administrators** can create and update student records, manage course curricula, post assignments with strict deadlines, inspect student submissions, grade work, and monitor real-time academic analytics through a dedicated administrative console.
- **Unit 6 Demonstration Lab:** An interactive laboratory page demonstrating HTTP state management—setting and retrieving client-side cookies (theme preferences, custom cookies) and server-side sessions (visit counters, session IDs, session flush).

---

## 2. Main Objectives

1. **Complete Syllabus Demonstration:** Provide a working, testable implementation for every unit (Units I to VI) of the INT253 course syllabus.
2. **Pure Traditional Django:** Utilize function-based views (FBVs), Django Template Language (DTL), ModelForms, and built-in Django Authentication without REST frameworks or modern frontend build tools.
3. **Robust Data Persistence:** Implement relational database modeling with `OneToOneField`, `ForeignKey`, and `ManyToManyField` relationships with cascade integrity in SQLite.
4. **Security & Validation:** Enforce server-side data validation (phone formats, registration number uniqueness, deadline checks, max marks bounds) and CSRF protection on all forms.
5. **Beginner-Friendly & Well-Documented:** Provide clean, commented Python and HTML code with complete automated unit and integration tests.

---

## 3. Software Requirements

- **Python:** Version 3.10, 3.11, or 3.12
- **Django:** Version 5.0+ or 6.x
- **Database:** SQLite 3 (built-in with Python)
- **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari
- **Dependencies:** Listed in `requirements.txt` (asgiref, Django, sqlparse, tzdata)

---

## 4. Installation Steps

### Step 1: Clone or Navigate to the Workspace Directory
```bash
cd "Student Course & Assignment Management System"
```

### Step 2: (Optional) Create and Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Seed Demo Academic Data (One-Step Setup)
Populate the database with pre-configured faculty accounts, students, courses, assignments, and sample graded submissions:
```bash
python seed_demo_data.py
```

### Step 6: Start the Development Server
```bash
python manage.py runserver
```
Open your web browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 5. Pre-Configured Demo Accounts for Viva

| Role | Username | Password | Notes |
|---|---|---|---|
| **Faculty / Admin** | `admin` | `admin123` | Full access to Admin Console & Django Admin |
| **Student 1** | `student1` | `pass123` | Aarav Sharma (Reg: 12200101, Dept: CSE) |
| **Student 2** | `student2` | `pass123` | Priya Patel (Reg: 12200205, Dept: IT) |
| **Student 3** | `student3` | `pass123` | Rohan Verma (Reg: 12200312, Dept: CSE) |

---

## 6. Project Architecture & Directory Structure

```
Student Course & Assignment Management System/
│
├── manage.py                          # Django administrative CLI runner
├── requirements.txt                   # Project package dependencies
├── seed_demo_data.py                  # Database populator script for viva
├── shell_demo.py                      # Interactive ORM demonstration script
├── README.md                          # Comprehensive project documentation
├── INT253_SYLLABUS_MAPPING.md         # Topic-by-topic course syllabus mapping
├── db.sqlite3                         # SQLite3 relational database
│
├── student_management/                # Project Configuration Package
│   ├── __init__.py
│   ├── settings.py                   # Global settings (APPS, DIRS, SESSIONS, COOKIES)
│   ├── urls.py                       # Root URLconf + 404/500 error handlers
│   ├── wsgi.py                       # Web Server Gateway Interface entrypoint
│   └── asgi.py                       # Asynchronous Server Gateway Interface
│
├── accounts/                          # Module 6: Authentication, Sessions & Cookies
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py         # Global template variables (theme, visits)
│   ├── forms.py                      # UserRegistrationForm, LoginForm, CookieDemoForm
│   ├── models.py                     # Auth User integration
│   ├── tests.py                      # 7 automated tests for Auth & Sessions
│   ├── urls.py                       # /accounts/ routes
│   └── views.py                      # Login, Register, Logout, Profile, Dashboards, Lab
│
├── students/                          # Module 5 & 2: Student Model & Profile CRUD
│   ├── admin.py                      # StudentAdmin with fieldsets and filters
│   ├── apps.py
│   ├── forms.py                      # StudentForm with phone & reg validation
│   ├── models.py                     # Student model (Reg No, Dept, Email, Phone)
│   ├── tests.py                      # 6 automated tests for Student views & regex
│   ├── urls.py                       # Path converters (<int:pk>) & regex routes
│   └── views.py                      # FBVs: list, detail, create, update, delete
│
├── courses/                           # Module 5 & 2: Course Curriculum & Enrollments
│   ├── admin.py                      # CourseAdmin with filter_horizontal
│   ├── apps.py
│   ├── forms.py                      # CourseForm, CourseEnrollmentForm
│   ├── models.py                     # Course model (ManyToMany with Student)
│   ├── tests.py                      # 5 automated tests for Course enrollment & cookies
│   ├── urls.py                       # Path converters & code regex (/code/<course_code>/)
│   └── views.py                      # Catalog, detail, enrollment, unenrollment
│
├── assignments/                       # Module 4 & 5: Assignments & Submissions
│   ├── admin.py                      # AssignmentAdmin & SubmissionAdmin
│   ├── apps.py
│   ├── forms.py                      # AssignmentForm, SubmissionForm, GradingForm
│   ├── models.py                     # Assignment & Submission models (ForeignKeys)
│   ├── tests.py                      # 6 automated tests for Submissions & Grading
│   ├── urls.py                       # CRUD routes, submit, and grade endpoints
│   └── views.py                      # FBVs: list, detail, submit, grade, manage
│
├── templates/                         # Module 3: Django Template System (DTL)
│   ├── base.html                     # Common layout (Navbar, Messages, Footer)
│   ├── home.html                     # Public hero landing page & stats
│   ├── 404.html                      # Custom Page Not Found error template
│   ├── 500.html                      # Custom Internal Server Error template
│   ├── accounts/
│   │   ├── login.html                # User login page
│   │   ├── register.html             # Student account registration page
│   │   ├── profile.html              # Student profile management page
│   │   └── session_cookie_demo.html  # Unit 6 Interactive Cookie & Session Lab
│   ├── dashboard/
│   │   ├── student_dashboard.html    # Student dashboard with stats & due tasks
│   │   └── admin_dashboard.html      # Faculty console with grading workflow
│   ├── students/
│   │   ├── student_list.html         # Directory with search & department filter
│   │   ├── student_detail.html       # Full profile, courses, and submission history
│   │   ├── student_form.html         # Create/Edit student record
│   │   └── student_confirm_delete.html# Safe deletion confirmation
│   ├── courses/
│   │   ├── course_list.html          # Responsive catalog grid with enroll buttons
│   │   ├── course_detail.html        # Syllabus, assignment list, enrolled peers
│   │   ├── course_form.html          # Create/Edit course syllabus
│   │   └── course_confirm_delete.html# Deletion confirmation
│   └── assignments/
│       ├── assignment_list.html      # Filter by course, active/past due status
│       ├── assignment_detail.html    # Guidelines, deadline countdown, submissions
│       ├── assignment_form.html      # Post new assignment with deadline
│       ├── assignment_confirm_delete.html # Deletion confirmation
│       ├── submission_form.html      # Submit solution with file upload
│       └── submission_grade.html     # Faculty evaluation & grading form
│
└── static/                            # Static Assets
    ├── css/
    │   └── custom.css                # Themes (Light, Dark, Blue), stat cards
    └── js/
        └── custom.js                 # Auto-dismiss alerts & Bootstrap tooltips
```

---

## 7. Database Design & Entity-Relationship (ER) Architecture

The database is structured around four primary models plus Django's built-in `auth_user`:

```
+---------------------------------------------------------------+
|                      django.contrib.auth                      |
|                             User                              |
+---------------------------------------------------------------+
                                 | 1
                                 | (OneToOneField)
                                 v 1
+---------------------------------------------------------------+
|                       students.Student                        |
+---------------------------------------------------------------+
| - id (PK)                                                     |
| - name (CharField)                                            |
| - email (EmailField, unique)                                  |
| - phone (CharField)                                           |
| - registration_number (CharField, unique)                    |
| - department (CharField, choices)                             |
| - join_date (DateField)                                       |
+---------------------------------------------------------------+
         | 1                                        ^ *
         |                                          |
         | (ForeignKey)                             | (ManyToManyField:
         v *                                        |  enrolled_courses)
+-----------------------------------+               |
|      assignments.Submission       |               |
+-----------------------------------+               |
| - id (PK)                         |               |
| - student_id (FK -> Student)      |               |
| - assignment_id (FK -> Assignment)|               |
| - submission_date (DateTimeField) |               |
| - submission_text (TextField)     |               |
| - attachment (FileField)          |               |
| - status (Submitted|Late|Graded)  |               |
| - marks_obtained (PositiveInt)    |               |
| - feedback (TextField)            |               |
+-----------------------------------+               |
         ^ *                                        |
         | (ForeignKey)                             |
         | 1                                        |
+-----------------------------------+               |
|       assignments.Assignment      |               |
+-----------------------------------+               |
| - id (PK)                         |               |
| - course_id (FK -> Course)        |               |
| - assignment_title (CharField)    |               |
| - description (TextField)         |               |
| - deadline (DateTimeField)        |               |
| - max_marks (PositiveInt)         |               |
+-----------------------------------+               |
         | *                                        |
         | (ForeignKey)                             |
         v 1                                        |
+---------------------------------------------------+-----------+
|                         courses.Course                        |
+---------------------------------------------------------------+
| - id (PK)                                                     |
| - course_name (CharField)                                      |
| - course_code (CharField, unique)                             |
| - description (TextField)                                     |
| - credits (PositiveSmallInt)                                  |
| - department (CharField, choices)                             |
| - students (ManyToManyField -> Student)                       |
+---------------------------------------------------------------+
```

### Relational Schema Characteristics
1. **Student - User:** `OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')`. Enables Django authentication while keeping student academic details modular.
2. **Course - Student:** `ManyToManyField(Student, related_name='enrolled_courses', blank=True)`. Represents the N:M relationship of multiple students enrolling in multiple courses.
3. **Course - Assignment:** `ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')`. Represents 1:N relationship where each assignment belongs to one course.
4. **Assignment - Student - Submission:** `Submission` has ForeignKeys to both `Student` and `Assignment`. It enforces `unique_together = ('student', 'assignment')` so each student has one recorded submission record per assignment.

---

## 8. Essential Django `manage.py` Commands

| Command | Purpose & Description |
|---|---|
| `python manage.py runserver` | Starts the local HTTP development server at `127.0.0.1:8000`. |
| `python manage.py makemigrations` | Scans `models.py` files and creates migration blueprint files in `<app>/migrations/`. |
| `python manage.py migrate` | Executes pending migrations against SQLite, creating and altering tables. |
| `python manage.py createsuperuser` | Prompts to create an administrative user with full permissions. |
| `python manage.py test` | Runs the automated Django test runner across all test cases (24 tests included). |
| `python manage.py shell` | Opens the interactive Python shell with the full Django environment loaded. |
| `python manage.py check` | Inspects the entire codebase for configuration bugs or URL errors without running server. |
| `python manage.py showmigrations` | Lists all migrations and displays their applied status `[X]`. |
| `python manage.py sqlmigrate <app> <num>` | Outputs the raw SQL queries that a specific migration generates. |

---

## 9. Comprehensive Testing Guide & Verification

### Running the Automated Test Suite
To execute all 24 automated test cases covering authentication, views, forms, models, cookies, sessions, and routing:
```bash
python manage.py test
```
**Expected Output:**
```
Found 24 test(s).
Creating test database for alias 'default'...
........................
----------------------------------------------------------------------
Ran 24 tests in 33.593s

OK
Destroying test database for alias 'default'...
```

### Running the ORM Shell Demonstration Script
To demonstrate Django ORM queries (Insert, Filter, icontains, Aggregates, Relations, Updates, Deletions) during viva:
```bash
python shell_demo.py
```

---

## 10. Manual Testing & Feature Walkthrough

### Scenario A: Testing Student Workflow
1. Navigate to `http://127.0.0.1:8000/accounts/login/`.
2. Login with student credentials: `student1` / `pass123`.
3. You will land on the **Student Dashboard** (`/dashboard/`).
4. Notice your name (**Aarav Sharma**), registration number, session visit count, and enrolled courses.
5. Click **"Courses"** in the top navigation bar.
6. Browse to **Cloud Computing (INT306)** and click **"Enroll"**.
7. Go to **"Assignments"** in the navigation bar. Click **"Lab 1: Django Architecture"** and click **"Submit Solution"**.
8. Enter your solution notes in the textarea and optionally upload a test file, then click **"Confirm Submission"**.
9. Notice the instant success notification and the updated status on your dashboard!

### Scenario B: Testing Faculty Workflow
1. Log out or open a private window, then navigate to `http://127.0.0.1:8000/accounts/login/`.
2. Login with faculty credentials: `admin` / `admin123`.
3. You will be redirected to the **Faculty Console** (`/admin-dashboard/`).
4. View the table of **"Submissions Awaiting Evaluation"**.
5. Click **"Grade Now"** next to an ungraded student submission.
6. Enter marks (e.g., `95` out of `100`), select status `Graded`, provide qualitative remarks, and click **"Submit Evaluation"**.
7. The submission is updated in the database, and the pending grading counter decreases.

### Scenario C: Testing Unit 6 Cookie & Session Lab
1. Click **"Unit 6 Lab (Cookies & Sessions)"** in the top navigation bar (`/accounts/session-cookie-demo/`).
2. **Sessions Demo:**
   - Click **"Increment Counter (+1)"**. Notice the session counter increases and the raw session dictionary updates in real time.
3. **Cookies Demo:**
   - Select **"Dark Slate Theme"** from the dropdown and click **"Set HTTP Cookie"**.
   - The response sets the `theme_preference` cookie, and the page immediately re-renders in dark mode!
   - Select **"University Blue Theme"** to change it to blue.
   - Set a custom cookie: Key `favorite_subject`, Value `Python Django`. Verify it appears under browser cookies!
   - Click **"Clear Cookies"** to delete custom demonstration cookies.

---

## 11. Security & Best Practices Implemented

- **CSRF Protection:** Every POST form includes the `{% csrf_token %}` tag, protecting against Cross-Site Request Forgery.
- **Server-Side Validation:** All forms implement custom validation logic in `clean_<fieldname>()` methods; client-side tampering is prevented.
- **POST-Redirect-GET (PRG) Pattern:** All successful POST operations redirect to a GET endpoint to prevent accidental form resubmissions on page refresh.
- **Password Hashing:** Passwords are never stored in plaintext; Django hashes them using PBKDF2 with SHA-256 and salt.
- **Authentication Decorators:** Sensitive views use the `@login_required` decorator and check `is_staff` permissions before granting administrative access.
- **Custom Error Handling:** Custom 404 (Not Found) and 500 (Internal Error) handlers deliver user-friendly, branded feedback.

---

## 12. University Viva & Examination FAQ

**Q1: What is the MVT architecture in Django?**  
- **Model:** Python classes in `models.py` mapping to database tables via Django ORM.
- **View:** Python functions in `views.py` containing business logic, receiving `HttpRequest`, and returning `HttpResponse`.
- **Template:** Presentation files in `templates/` rendering dynamic HTML using the Django Template Language (DTL).

**Q2: What is the difference between a Cookie and a Session?**  
- A **Cookie** is stored on the client browser (max 4 KB), transmitted back and forth in HTTP headers.
- A **Session** stores data on the web server (in SQLite's `django_session` table). Only a random 32-character `sessionid` cookie is stored in the browser.

**Q3: Why use `reverse()` or `{% url %}` instead of hardcoded paths?**  
- Using URL names decouples URLs from view definitions. If a URL pattern is updated in `urls.py`, all templates and view redirects update automatically without breaking links.

**Q4: How does Django prevent SQL Injection?**  
- Django's ORM parameterizes all SQL queries automatically when using methods like `.filter()`, `.get()`, and `.create()`. User inputs are never directly concatenated into raw SQL strings.

