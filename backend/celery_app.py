from celery import Celery
from celery.schedules import crontab

# Define the Celery app instance once
celery = Celery('parking_app')

# Apply base configuration
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    timezone='UTC',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,

    include=['tasks'],
    beat_schedule={
        'daily-parking-reminders': {
            'task': 'tasks.send_daily_reminders',
            'schedule': 600.0,  
            # 'schedule': crontab(hour=18, minute=0),  # Daily at 6:00 PM
        },
        'monthly-activity-reports': {
            'task': 'tasks.send_monthly_reports',
            'schedule': 10.0,  
            # 'schedule': crontab(day_of_month=1, hour=9, minute=0),  # Monthly at 9:00 AM on the 1st
        },
    }
)

def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    
    # Import tasks to register them with the app
    import tasks
    
    return celery

