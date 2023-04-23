from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
import datetime

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.contrib.auth import (
    login,
    authenticate,
    logout
)

#HELPER
from MultiVendor.helper import (
    check_if_customer,
    check_if_vendor,
    get_vendor
)

#MODEL
from accounts.models import (
    UserProfile
)
from orders.models import (
    Order
)

#FORMS
from .forms import (
    UserForm
)
from vendor.forms import (
    VendorForm
)

# Create your views here.
def register_customer(request):
    if request.user.is_authenticated:
        messages.info(request, 'you are already logged in!')
        return redirect('my-account')
    
    elif request.method == 'POST':        
        form = UserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            password = form.cleaned_data['password']
            instance.role = 2
            instance.set_password(password)
            instance.is_active = True
            instance.save() 
            messages.success(request, 'registered successfully!')
            return redirect('login')
        else:
            messages.error(request, 'check out the errors')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register/customer.html', context)

def register_vendor(request):
    if request.user.is_authenticated:
        messages.info(request, 'you are already logged in!')
        return redirect('my-account')
    
    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST,request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            user_instance = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            user_instance.role = 1
            user_instance.is_active = True
            user_instance.set_password(password)
            user_instance.save()
            
            # UserProfile
            user_profile = UserProfile.objects.get(user=user_instance)
            
            vendor_instance = vendor_form.save(commit=False)
            vendor_instance.user = user_instance
            vendor_instance.user_profile = user_profile
            vendor_instance.is_approved = True
            vendor_instance.save()

            messages.success(request, 'successfully registered!')
            return redirect('login')
        else:
            messages.error(request, 'check out the errors')
            print(user_form.errors)
            print(vendor_form.errors) 
    else:
        user_form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': user_form,
        'v_form': vendor_form
    }
    return render(request, 'accounts/register/vendor.html', context)

def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'you are already logged in!')
        return redirect('my-account')
    
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'logged in successfully')
            return redirect('my-account')
        else:
            messages.error(request, 'checkout errors')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
@user_passes_test(check_if_customer)
def customer_dashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    orders_count = orders.count()
    recent_orders = orders[:5]
    context = {
        'orders_count': orders_count,
        'recent_orders': recent_orders
    }
    return render(request, 'accounts/dashboard/customer.html', context)


@login_required(login_url='login')
@user_passes_test(check_if_vendor)
def vendor_dashboard(request):
    vendor = get_vendor(request)['get_vendor']
    orders = Order.objects.filter(vendors__in=[vendor.id])

    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']
    

    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']
    context = {
        'orders_count': orders.count(),
        'recent_orders': orders[0:5],
        'current_month_revenue':current_month_revenue,
        'total_revenue':total_revenue
        

    }
    return render(request, 'accounts/dashboard/vendor.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('login')
