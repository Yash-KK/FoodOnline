from django.shortcuts import render, redirect
from django.contrib import messages
import json
from MultiVendor.helper import (
    get_user_profile
)

#MODEL
from orders.models import (
    Order,
    OrderedFood
)

#FORMS
from accounts.forms import (
    ProfileSettingUserForm,
    UserProfileForm
)
# Create your views here.
def profile_settings(request):
    if request.method == 'POST':
        user_form = ProfileSettingUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=get_user_profile(request)['get_user_profile'])
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('profile-setting')
        else:
            messages.error(request, 'checkout the')
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = ProfileSettingUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=get_user_profile(request)['get_user_profile'])
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': get_user_profile(request)['get_user_profile']
    }
    return render(request, 'customer/profileSetting.html', context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    context = {
        'orders': orders
    }
    return render(request, 'customer/myOrders.html', context)


def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)

    tax_data = json.loads(order.tax_data)
    subtotal = order.total - order.total_tax
    ordered_food = OrderedFood.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_food': ordered_food,
        'subtotal': subtotal,
        'tax_data': tax_data
    }
    return render(request, 'customer/orderDetail.html', context)
