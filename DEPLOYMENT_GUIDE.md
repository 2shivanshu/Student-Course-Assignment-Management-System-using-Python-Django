# Cloud Deployment Guide: Student Course & Assignment Management System

This guide explains how to deploy your Django project to the cloud for free so you have a live public URL (e.g. `https://student-management-system.onrender.com`) to demonstrate to your university examiner and faculty.

The project is already pre-configured for **Render.com**, **Railway.app**, and **PythonAnywhere** with:
- `Procfile` (WSGI web server configuration)
- `build.sh` (automatic dependency installation, migrations, static files collection, and database seeding)
- `render.yaml` (one-click infrastructure blueprint)
- `whitenoise` (zero-configuration static assets handling in production)

---

## Option 1: Deploy on Render.com (Recommended — 100% Free & Simplest)

Render connects directly to your GitHub repository and automatically detects Python Django.

### Step 1: Sign Up / Sign In
1. Go to [https://render.com/](https://render.com/).
2. Click **Get Started for Free** or **Sign In**.
3. Choose **Sign in with GitHub** (use the same GitHub account `2shivanshu`).

### Step 2: Create a New Web Service
1. In your Render Dashboard, click the blue **"New +"** button at the top-right.
2. Select **"Web Service"**.
3. Select **"Build and deploy from a Git repository"** and click **Next**.
4. Choose your repository:
   - `Student-Course-Assignment-Management-System-using-Python-Django`
   - *(If it does not appear in the list, click "Configure account" to grant Render access to your GitHub repositories).*
5. Click **"Connect"**.

### Step 3: Configure Settings (Render auto-fills most of this!)
Fill or verify the following fields:
- **Name:** `student-management-system` *(or any unique name you prefer)*
- **Region:** Any (e.g., `Singapore` or `Frankfurt` or `Oregon`)
- **Branch:** `main`
- **Root Directory:** *(leave blank)*
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn student_management.wsgi:application`
- **Instance Type:** Select **Free** ($0 / month)

### Step 4: Click "Create Web Service"
1. Scroll down and click **"Create Web Service"**.
2. Render will trigger the build:
   - It runs `build.sh`: installs dependencies, applies migrations, collects static files, and seeds the sample faculty & student accounts.
   - It starts `gunicorn`.
3. In about 2-3 minutes, you will see:
   `==> Your service is live 🎉`
4. Render displays your live public URL at the top left, for example:  
   👉 **`https://student-management-system.onrender.com`**

---

## Option 2: Deploy on Railway.app

1. Go to [https://railway.app/](https://railway.app/) and sign in with GitHub.
2. Click **"New Project"** -> **"Deploy from GitHub repo"**.
3. Select `Student-Course-Assignment-Management-System-using-Python-Django`.
4. Railway will automatically detect the `Procfile` and deploy the service.
5. In project settings, click **"Generate Domain"** to get a public `*.up.railway.app` URL.

---

## Option 3: Deploy on PythonAnywhere

1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/) and register a free Beginner account (e.g., username `shivanshu`).
2. Open a **Bash Console** and clone your repo:
   ```bash
   git clone https://github.com/2shivanshu/Student-Course-Assignment-Management-System-using-Python-Django.git
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   cd Student-Course-Assignment-Management-System-using-Python-Django
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python seed_demo_data.py
   ```
4. Go to the **Web** tab in PythonAnywhere dashboard:
   - Click **"Add a new web app"** -> **Manual Configuration** -> **Python 3.10/3.11**.
   - Set **Virtualenv path** to: `/home/shivanshu/Student-Course-Assignment-Management-System-using-Python-Django/venv`
   - Open the **WSGI configuration file** and update it:
     ```python
     import os
     import sys
     path = '/home/shivanshu/Student-Course-Assignment-Management-System-using-Python-Django'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'student_management.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - Click the green **Reload** button.
5. Your app is live at: `https://shivanshu.pythonanywhere.com`.

---

## Testing Your Deployed Live Portal

Once deployed, open your live URL and test:
1. **Public Landing Page:** `https://your-app-url.onrender.com/`
2. **Faculty Login:** `admin` / `admin123` -> Redirects to Faculty Console!
3. **Student Login:** `student1` / `pass123` -> Redirects to Student Dashboard!
4. **Unit 6 Cookies & Sessions:** `https://your-app-url.onrender.com/accounts/session-cookie-demo/`
