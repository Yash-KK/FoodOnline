from django.db import models
from django.utils.text import slugify
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#MODEL
from accounts.models import (
    User,
    UserProfile
)
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='vendor')

    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=25, unique=True)
    license = models.ImageField(upload_to="Gallery/Vendor/License")
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + '-' + get_random_string(4)
        super(Vendor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendor's"
        
    def __str__(self):
        return f"{self.name}"
    