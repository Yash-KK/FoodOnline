from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#HELPER
from MultiVendor.helper import (
    get_vendor,
    get_user_profile
)

#FORMS
from .forms import (
    VendorForm,
    OpeningHourForm
)
from accounts.forms import (
    UserProfileForm,
)

#MODEL
from .models import (
    OpeningHour
)

# Create your views here.
@login_required(login_url='login')
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

@login_required(login_url='login')
def opening_hour(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        day = request.POST.get('day')
        from_hour = request.POST.get('from_hour')
        to_hour = request.POST.get('to_hour')
        is_closed = request.POST.get('is_closed')

        if is_closed == 'false':
            is_closed = False
        else:
            is_closed = True
        try:
            opening_hour = OpeningHour.objects.create(vendor=get_vendor(request)['get_vendor'], day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
            opening_hour.save()
        
            return JsonResponse({
                'success': "Opening Hour instance created",
                'id': opening_hour.id,
                'from_hour': opening_hour.from_hour,
                'to_hour': opening_hour.to_hour,
                'is_closed': opening_hour.is_closed,
                'day': opening_hour.day
            })
        except:
            return JsonResponse({
                'error': "You must have entered already existing fields!"
            })


    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request)['get_vendor'])
    form = OpeningHourForm()
    context = {
        'opening_hours': opening_hours,
        'form': form
    }
    return render(request, 'vendor/openingHour.html', context)

def remove_opening_hour(request, hour_id):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        opening_hour = OpeningHour.objects.get(id=hour_id)
        opening_hour.delete()
        return JsonResponse({
            'info': 'deleted hour instance',
            'hour_id': hour_id
        })
    else:
        return JsonResponse({
            'error': "Not an Ajax Request"
        })
