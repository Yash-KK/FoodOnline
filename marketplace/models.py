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
