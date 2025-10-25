@echo off
echo ========================================================================
echo FOSS Treasure Hunt - Django Backend Setup
echo ========================================================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo.

echo Step 2: Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo Error creating migrations!
    pause
    exit /b 1
)
echo.

echo Step 3: Applying migrations...
python manage.py migrate
if errorlevel 1 (
    echo Error applying migrations!
    pause
    exit /b 1
)
echo.

echo Step 4: Setting up default data...
python setup_database.py
if errorlevel 1 (
    echo Error setting up default data!
    pause
    exit /b 1
)
echo.

echo ========================================================================
echo Setup Complete! 🎉
echo ========================================================================
echo.
echo Next steps:
echo 1. Create admin user: python manage.py createsuperuser
echo 2. Start server: python manage.py runserver
echo 3. Access admin: http://localhost:8000/admin/
echo.
pause
