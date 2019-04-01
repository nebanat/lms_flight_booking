from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'(?P<flight_pk>\d+)/reserve/$', views.FlightBookingView.as_view())
]
