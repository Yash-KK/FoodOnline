from django.urls import path

#VIEWS
from MultiVendor.helper import (
    my_account
)
from .views import (
    register_customer,
    register_vendor,

    login_user,

    customer_dashboard,
    vendor_dashboard,

    logout_user
)
urlpatterns = [
    path('register-customer/', register_customer, name='register-customer'),
    path('register-vendor/', register_vendor, name='register-vendor'),

    path('login-user/', login_user, name='login'),

    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard/', vendor_dashboard, name='vendor-dashboard'),

    path('logout-user/',logout_user, name='logout'),

    path('my-account/', my_account, name='my-account')
]
