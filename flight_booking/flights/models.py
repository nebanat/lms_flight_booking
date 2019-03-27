from django.db import models


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
