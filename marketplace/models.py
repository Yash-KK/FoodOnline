from django.db import models

#MODEL
from accounts.models import (
    User
)
from menu.models import (
    FoodItem
)
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = "Cart's"
        
    def __str__(self):
        return f"{self.fooditem}: {self.quantity}"

class Tax(models.Model):
    tax_type = models.CharField(max_length=5, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage(%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"
        

    def __str__(self):
        return f"{self.tax_type}: {self.tax_percentage}"
    
