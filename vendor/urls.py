from django.urls import path

from .views import (

    my_restaurant,

    opening_hour,
    remove_opening_hour
)
urlpatterns = [
    path('my-restaurant/', my_restaurant, name='my-restaurant'),
    path('opening-hour/', opening_hour, name='opening-hour'),
    path('remove-opening-hour/<int:hour_id>/', remove_opening_hour, name='remove-opening-hour')
]
