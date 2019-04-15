from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<flight_pk>\d+)/reserve/$', views.FlightBookingView.as_view()),
    url(r'(?P<flight_pk>\d+)/passengers/$', views.FlightPassengers.as_view())
]
