from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from MultiVendor.settings import GOOGLE_API_KEY
from decimal import Decimal

#MODEL
from vendor.models import (
    Vendor,
    UserProfile
)
from marketplace.models import (
    Cart,
    Tax
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
    subtotal, tax_amount ,grand_total = 0,0,0
    tax_dict = {}
    try:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += (item.quantity * Decimal(item.fooditem.price))
    except:
        subtotal, grand_total = 0,0
    
    tax_instance = Tax.objects.all()
    for i in tax_instance:
        tax_type = i.tax_type
        tax_percentage = i.tax_percentage
        tax_amount = round((tax_percentage * subtotal)/100, 2)
        tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}}) 
    tax_amount = sum(float(j) for value in tax_dict.values() for j in value.values())


    return {
        'subtotal': subtotal,        
        'grandtotal': float(subtotal) + float(tax_amount),
        'tax_dict': tax_dict
    }
