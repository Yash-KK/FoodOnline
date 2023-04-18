from django.db import models
from django.utils.text import slugify

import random
import string


def get_food_item_image_path(instance, filename):
    vendor_id = instance.vendor.id
    return f'Gallery/food_item_images/vendor_{vendor_id}/{filename}'



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#MODEL
from vendor.models import (
    Vendor
)

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStamp):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=30, unique=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + '-' + get_random_string(4)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.name}'

class FoodItem(TimeStamp):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='fooditems')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True)
    description = models.TextField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to=get_food_item_image_path)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.food_title) + '-' + get_random_string(4)
        super(FoodItem, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Food Item"
        verbose_name_plural = "Food Item's"

    def __str__(self):
        return f"{self.food_title}"
    
    