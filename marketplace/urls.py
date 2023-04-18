from django.urls import path

from .views import (
    marketplace,
    listing_detail
)
urlpatterns = [
    path('listing/', marketplace, name='marketplace'),
    path('listing-detail/<slug:vendor_slug>/', listing_detail, name='listing-detail') 
]
