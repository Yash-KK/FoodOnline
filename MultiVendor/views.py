from django.shortcuts import render
from django.db.models import Q

from vendor.models import (
    Vendor
)
from menu.models import (
    FoodItem
)

def home(request):
    vendors = Vendor.objects.filter(is_approved=True)
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)


def search(request):
    keyword = request.GET['keyword']    
    vendor_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword).values_list('vendor', flat=True)    
    vendors = Vendor.objects.filter(
        Q(id__in=vendor_by_fooditems)| 
        Q(name__icontains=keyword)
    )
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count        
    }
    return render(request, 'marketplace/listing.html', context)
