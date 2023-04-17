from django.shortcuts import render,redirect
from django.contrib import messages


#HELPER
from MultiVendor.helper import (
    get_vendor,
    get_user_profile
)

#FORMS
from .forms import (
    VendorForm
)
from accounts.forms import (
    UserProfileForm,
)


# Create your views here.
def my_restaurant(request):
    vendor = get_vendor(request)['get_vendor']   
    user_profile = get_user_profile(request)['get_user_profile']     
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'restaurant updated')
            return redirect('my-restaurant')
        else:
            messages.error(request, 'checkout errors')
            print(vendor_form.errors)
            print(profile_form.errors)

    else:
        profile_form = UserProfileForm(instance=user_profile)
        vendor_form = VendorForm(instance=vendor)
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,


        'vendor': vendor
    }
    return render(request, 'vendor/myRestaurant.html', context)

