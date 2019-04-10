from django.contrib.auth import get_user_model
from celery import shared_task

from .helpers.email import send_ticket_reminder

User = get_user_model()


@shared_task
def send_flight_remainder_task():
    return send_ticket_reminder()
