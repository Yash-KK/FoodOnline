from django.urls import path

from .views import (
    profile_settings,
    my_orders,
    order_detail
)
urlpatterns = [
    path('profile-setting/', profile_settings, name='profile-setting'),
    path('my-orders/', my_orders, name='my-orders'),
    path('<str:order_number>/', order_detail, name='order-detail')
]
