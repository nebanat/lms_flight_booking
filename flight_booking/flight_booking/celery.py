import os
from celery import Celery

# set django default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')

# configure celery
app = Celery('flight_booking')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # auto discover taska

