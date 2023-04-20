from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date

from MultiVendor.helper import (
    get_cart_count,
    get_tax_dict
)

#MODEL
from vendor.models import (
    Vendor,
    OpeningHour
)
from menu.models import (
    Category,
    FoodItem
)
from .models import (
    Cart
)

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True)
    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listing.html', context)

def listing_detail(request, vendor_slug):
    vendor = Vendor.objects.get(slug=vendor_slug)

    try:
        opening_hours = OpeningHour.objects.filter(vendor=vendor)

        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()        
        current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    except:
        opening_hours = None

    try:
        cartitems = Cart.objects.filter(user=request.user)
    except:
        cartitems = None
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'categories': categories,        
        'cartitems': cartitems,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours
    }
    return render(request, 'marketplace/listingDetail.html', context)



def add_to_cart(request, food_id):    
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    cartitem = Cart.objects.get(fooditem=fooditem, user=request.user)
                    cartitem.quantity +=1
                    cartitem.save()
                    return JsonResponse({
                        'success': "Increased the quantity!",
                        'cart_count': get_cart_count(request)['get_cart_count'],
                        'quantity': cartitem.quantity,
                        'tax_data': get_tax_dict(request)
                        
                    })
                except:
                    cartitem = Cart.objects.create(fooditem=fooditem, quantity=1, user=request.user)
                    cartitem.save()
                    return JsonResponse({
                        'success': "Created a cart item",
                        'cart_count': get_cart_count(request)['get_cart_count'],
                        'quantity': 1,
                        'tax_data': get_tax_dict(request)
                       
                    })
            except FoodItem.DoesNotExist:
                messages.error(request, 'Food Item does not exist!')
                return redirect('home')

        else:
            return JsonResponse({
                'error': "Request is not AJAX"
            })

    else:
        return JsonResponse({
            'login_required': 'Please Login to continue'
        })


def decrease_cart(request, food_id):    
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    cartitem = Cart.objects.get(fooditem=fooditem, user=request.user)
                    if cartitem.quantity == 1:
                        cartitem.delete()
                        return JsonResponse({
                            'success': "cart item deleted",
                            'cart_count': get_cart_count(request)['get_cart_count'],
                            'quantity': 0,
                            'tax_data': get_tax_dict(request)
                            
                        })
                    else:
                        cartitem.quantity -=1
                        cartitem.save()
                        return JsonResponse({
                            'success': "quantity decreased",
                            'cart_count': get_cart_count(request)['get_cart_count'],
                            'quantity': cartitem.quantity,
                            'tax_data': get_tax_dict(request)
                         
                        })
                except:
                    return JsonResponse({
                        'qty0':'Quantity already 0'
                    })

            except FoodItem.DoesNotExist:
                messages.error(request, 'Food Item does not exist!')
                return redirect('home')
        else:
            return JsonResponse({
                'error': "Request is not AJAX"
            })

    else:
        return JsonResponse({
            'login_required': 'Please Login to continue'
        })


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                cartitem = Cart.objects.get(id=cart_id)
                cartitem.delete()
                return JsonResponse({
                    'success': "cart item deleted",
                    'cart_count': get_cart_count(request)['get_cart_count'],
                    'cart_id': cart_id,
                    'tax_data': get_tax_dict(request)
                   
                })
            except:
                pass
        return JsonResponse({
            'error': 'request is not AJAX'
        })
    else:
        return JsonResponse({
            'login_required': "Please Login to continue!"
        })