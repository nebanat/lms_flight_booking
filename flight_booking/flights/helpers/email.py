from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .decorators import start_new_thread


@start_new_thread
def send_email_with_booked_flight_details(booking):
    html_content = render_to_string('flights/email.html', {'booking': booking})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives('Flight details', text_content, 'noreply@airtech.com', [booking.user.email])

    msg.attach_alternative(html_content, "text/html")
    msg.send()


