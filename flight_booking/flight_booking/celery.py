import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')

app = Celery('flight_booking')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

