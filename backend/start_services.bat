@echo off
echo Starting Parking App Services...

REM Start MailHog for email testing
echo Starting MailHog...
start "MailHog Server" mailhog.exe

REM Wait a moment for MailHog to start
timeout /t 2 /nobreak > nul

REM Start Redis server
echo Starting Redis server...
start "Redis Server" redis-server

REM Wait a moment for Redis to start
timeout /t 3 /nobreak > nul

REM Start Celery worker
echo Starting Celery worker...
start "Celery Worker" cmd /k "celery -A celery_app.celery worker --loglevel=info --pool=solo"

REM Wait a moment for Celery worker to start
timeout /t 3 /nobreak > nul

REM Start Celery beat scheduler
echo Starting Celery beat scheduler...
start "Celery Beat" cmd /k "celery -A celery_app.celery beat --loglevel=info"

echo All services started!
echo.
echo Services running:
echo - MailHog Server (http://localhost:8025 for email UI)
echo - Redis Server
echo - Celery Worker
echo - Celery Beat Scheduler
echo.
echo You can now start your Flask application with: python app.py
echo MailHog email interface: http://localhost:8025
pause
