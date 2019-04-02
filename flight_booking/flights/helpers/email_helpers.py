from threading import Thread
from functools import wraps
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def start_new_thread(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@start_new_thread
def send_email_with_booked_flight_details(booking):
    html_content = render_to_string('flights/email.html', {'booking': booking})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives('Flight details', text_content, 'noreply@airtech.com', [booking.user.email])

    msg.attach_alternative(html_content, "text/html")
    msg.send()

