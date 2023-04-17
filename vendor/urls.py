from django.urls import path

from .views import (
    my_restaurant
)
urlpatterns = [
    path('my-restaurant/', my_restaurant, name='my-restaurant')
]
