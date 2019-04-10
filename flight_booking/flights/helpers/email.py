from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mass_mail
from .decorators import start_new_thread

User = get_user_model()


@start_new_thread
def send_email_with_booked_flight_details(booking):
    html_content = render_to_string('flights/email.html', {'booking': booking})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives('Flight details', text_content, 'noreply@airtech.com', [booking.user.email])

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_ticket_reminder():
    date_time = timezone.now() + timedelta(days=1)
    passengers = User.objects.filter(
        booking__flight__departure_time__lte=date_time,
        booking__flight__departure_time__gte=timezone.now(),
        booking__booked=True
    )

    passengers_email = [passenger.email for passenger in passengers]

    msg_reminder = render_to_string('flights/flight_reminder.txt')

    reminder_message = ('Flight reminder',
                        msg_reminder,
                        'noreply@airtech.com',
                        passengers_email)
    send_mass_mail((reminder_message,), fail_silently=True)
