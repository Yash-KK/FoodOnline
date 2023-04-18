from django.shortcuts import render

#MODEL
from vendor.models import (
    Vendor
)
from menu.models import (
    Category,
    FoodItem
)

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listing.html', context)

def listing_detail(request, vendor_slug):
    vendor = Vendor.objects.get(slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'marketplace/listingDetail.html', context)

