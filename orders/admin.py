from django.contrib import admin

#MODEL
from .models import (
    Order,
    OrderedFood,
    Payment
)

# Register your models here.

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'payment','payment_method', 'status', 'is_ordered']
    inlines = [
        OrderedFoodInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
admin.site.register(Payment)
