from django.urls import path

from .views import (
    marketplace,
    listing_detail,

    add_to_cart,
    decrease_cart,
    delete_cart   
    
)
urlpatterns = [
    path('listing/', marketplace, name='marketplace'),
    path('listing-detail/<slug:vendor_slug>/', listing_detail, name='listing-detail'),

    path('add-to-cart/<int:food_id>/', add_to_cart, name='add-to-cart'),
    path('decrease-cart/<int:food_id>/', decrease_cart, name='decrease-cart'),
    path('delete-cart/<int:cart_id>/', delete_cart, name='delete-cart')
    
]
