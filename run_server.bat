@echo off
title Student Course & Assignment Management System - Server Launcher
echo ======================================================================
echo    Student Course & Assignment Management System (INT253 Project)
echo ======================================================================
echo.
echo Starting Django development server at http://127.0.0.1:8000/ ...
echo Press Ctrl+C in this terminal window to stop the server.
echo.
python manage.py runserver 127.0.0.1:8000
pause
