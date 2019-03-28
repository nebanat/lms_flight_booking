from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Flight(models.Model):
    """
     Flight model definition
    """
    from_location = models.CharField(
        max_length=100,
        verbose_name='From Location'
    )
    to_location = models.CharField(
        max_length=100,
        verbose_name='To Location'
    )
    departure_time = models.DateTimeField(
        verbose_name='Departure time'
    )
    arrival_time = models.DateTimeField(
        verbose_name='Arrival Time'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    no_of_seats = models.IntegerField()

    price = models.IntegerField(default=0)

    passengers = models.ManyToManyField(
        User,
        through='Booking',
        through_fields=('flight', 'user')
    )

    class Meta:
        ordering = ['created_at']


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=True, using=None,
             update_fields=None, *args, **kwargs):
        exist = Booking.objects.filter(user=self.user, flight=self.flight, booked=self.booked).count()
        if exist:
            from django.db import IntegrityError
            raise IntegrityError(
                "User has booked this flight already"
            )
        return super(Booking, self).save(*args, **kwargs)

