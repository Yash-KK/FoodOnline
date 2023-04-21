from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
import json, razorpay

from MultiVendor.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
)
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


from MultiVendor.helper import (
    get_user_profile,
    get_tax_dict
)

#FORM
from .forms import (
    OrderForm
)

#MODEL
from marketplace.models import (
    Cart
)
from orders.models import (
    Order,
    Payment,
    OrderedFood
)

# Create your views here.
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.count() == 0:
        messages.info(request, 'you have no cart items')
        return redirect('marketplace')
    
    data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': request.user.phone_number,
        'address': get_user_profile(request)['get_user_profile'].address_line,
        'country': get_user_profile(request)['get_user_profile'].country,
        'state': get_user_profile(request)['get_user_profile'].state,
        'city': get_user_profile(request)['get_user_profile'].city,
        'pin_code': get_user_profile(request)['get_user_profile'].pincode
    }
    order_form = OrderForm(initial=data)
    context = {
        'form': order_form
    }
    return render(request, 'marketplace/checkout.html', context)


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.count() == 0:
        messages.info(request, 'you have no cart items')
        return redirect('marketplace')
    
    tax_dict = get_tax_dict(request)['tax_dict']
    tax_amount = sum(float(j) for value in tax_dict.values() for j in value.values())


    today = date.today()
    if request.method == 'POST':        
        order = Order()
        order.first_name = request.POST['first_name']
        order.last_name = request.POST['last_name']
        order.phone = request.POST['phone']
        order.email = request.POST['email']
        order.address = request.POST['address']
        order.country = request.POST['country']
        order.state = request.POST['state']
        order.city = request.POST['city']
        order.pin_code = request.POST['pin_code']
        order.payment_method = request.POST['payment_method']

        order.user = request.user
        order.total = get_tax_dict(request)['grandtotal']
        order.tax_data = json.dumps(tax_dict)
        order.total_tax = tax_amount
        order.save()

        order.order_number = today.strftime('%Y-%m-%d') + '-' + str(order.id)
        order.save()

        DATA = {
            "amount": order.total*100,
            "currency": "INR",
            "receipt": f"receipt#{order.order_number}"            
        }
        razorpay_order = client.order.create(data=DATA)
        razorpay_order_id = razorpay_order['id']

        context = {
            'order': order,
            'cart_items': cart_items,

            'KEY_ID': RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order_id
        }
        return render(request, 'orders/placeOrder.html', context)
             
    return render(request, 'orders/placeOrder.html')


def payments(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        trans_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        order_number = request.POST.get('order_number')

        # Payment Instance
        payment = Payment()
        payment.user = request.user
        payment.transaction_id = trans_id
        payment.amount = amount
        payment.payment_method = payment_method
        payment.status = status
        payment.save()

        # Updating Order instance
        order = Order.objects.get(order_number=order_number)
        order.payment = payment
        order.status = "Accepted"
        order.is_ordered = True
        order.save()
        
        # Create OrderedFood Instance
        for item in cart_items:
            ordered_food = OrderedFood()        
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.quantity * item.fooditem.price
            ordered_food.save()
        
        # Cart item delete
        cart_items.delete()

        return JsonResponse({
            'trans_id': trans_id,
            'order_number': order_number
        })
def order_complete(request):    
    order_number = request.GET['order_no']
    trans_id = request.GET['trans_id']

    order = Order.objects.get(order_number=order_number)
    order.status = 'Completed'
    order.save()
    
    tax_data = json.loads(order.tax_data)
    subtotal = order.total - order.total_tax
    ordered_food = OrderedFood.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_food': ordered_food,
        'tax_data': tax_data,
        'subtotal': subtotal
    }
    return render(request, 'orders/orderComplete.html', context)
