from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from MultiVendor.settings import GOOGLE_API_KEY


#MODEL
from vendor.models import (
    Vendor,
    UserProfile
)
from marketplace.models import (
    Cart
)

def my_account(request):
    if request.user.role == 1:
        return redirect('vendor-dashboard')
    elif request.user.role == 2:
        return redirect('customer-dashboard')

def check_if_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_if_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Context Processors
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return {
        'get_vendor' : vendor
    }

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return {
        'get_user_profile': user_profile
    }

def get_google_api_key(request):   
    if GOOGLE_API_KEY:
        return {
            'GOOGLE_API_KEY': GOOGLE_API_KEY
        }
    return {
        'GOOGLE_API_KEY': None
    }

def get_cart_count(request):
    cart_count = 0
    try:        
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            cart_count += item.quantity
    except:
        cart_count = 0
    return {
        'get_cart_count': cart_count
    }

def get_tax_dict(request):
    subtotal, tax, grand_total = 0,0,0
    try:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += (item.quantity * item.fooditem.price)
    except:
        subtotal, grand_total = 0,0
    tax = (2.5/100) * subtotal
    grand_total = subtotal + tax
    return {
        'subtotal': subtotal,
        'tax': tax,
        'grandtotal': grand_total
    }