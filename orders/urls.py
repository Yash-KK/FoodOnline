from django.urls import path

from .views import (
    checkout,
    place_order,

    order_complete,
    payments
)
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('place-order/', place_order, name='place-order'),

    path('order-complete/', order_complete, name='order-complete'),
    path('payment/', payments, name='payments')
]
