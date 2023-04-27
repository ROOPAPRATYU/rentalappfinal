from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_application.settings')

app = Celery('rental_application')
app.conf.enable_utc=False
app.conf.update(timezone="Asia/kolkata")

app.config_from_object(settings, namespace='CELERY')
# using celery beat scheduler apply periodic scheduler
app.conf.beat_schedule={
    "sendwhatsappnotification":{
    "task":"notification.tasks.send_notification",
    "schedule":crontab(day_of_month=22,hour=14,minute=40)
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')