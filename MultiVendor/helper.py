from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from MultiVendor.settings import GOOGLE_API_KEY


#MODEL
from vendor.models import (
    Vendor,
    UserProfile
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
