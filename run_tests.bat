@echo off
title Student Management - Run Automated Unit Tests
echo ======================================================================
echo    Running Automated Django Test Suite (24 Test Cases)
echo ======================================================================
echo.
python manage.py test
echo.
pause
