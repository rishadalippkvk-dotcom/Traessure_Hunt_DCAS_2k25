@echo off
cls
echo.
echo ========================================================================
echo    FOSS TREASURE HUNT - QUICK DATABASE SETUP
echo ========================================================================
echo.
echo This script will create the database for your treasure hunt game!
echo.
pause

echo.
echo [1/4] Creating migration files...
python manage.py makemigrations authentication
if errorlevel 1 goto error

echo.
echo [2/4] Creating database tables...
python manage.py migrate
if errorlevel 1 goto error

echo.
echo [3/4] Loading default achievements...
python setup_database.py
if errorlevel 1 goto error

echo.
echo [4/4] Database setup complete!
echo.
echo ========================================================================
echo    SUCCESS! Database is ready to use.
echo ========================================================================
echo.
echo Database file created: treasure_hunt.db
echo.
echo NEXT STEPS:
echo.
echo 1. Create an admin user:
echo    python manage.py createsuperuser
echo.
echo 2. Start the Django server:
echo    python manage.py runserver
echo.
echo 3. Access the admin panel:
echo    http://localhost:8000/admin/
echo.
echo 4. Test the API endpoints:
echo    See SETUP_INSTRUCTIONS.md for examples
echo.
echo ========================================================================
goto end

:error
echo.
echo ========================================================================
echo    ERROR: Something went wrong!
echo ========================================================================
echo.
echo Please check the error messages above and try again.
echo.
echo Common issues:
echo - Missing dependencies: Run "pip install -r requirements.txt"
echo - Wrong directory: Make sure you're in the 'backend' folder
echo.
pause
exit /b 1

:end
pause
