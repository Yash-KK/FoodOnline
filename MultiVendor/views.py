from django.shortcuts import render

from vendor.models import (
    Vendor
)

def home(request):
    vendors = Vendor.objects.filter(is_approved=True)
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)

