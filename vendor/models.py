from django.db import models
from django.utils.text import slugify
from datetime import datetime, timedelta
import random, string


TIME_LIST = []
start_time = datetime(1900, 1, 1, hour=0, minute=0)
end_time = datetime(1900, 1, 2, hour=0, minute=0)
while start_time < end_time:
    time_str = start_time.strftime('%I:%M %p')
    TIME_LIST.append((time_str, time_str))
    start_time += timedelta(minutes=30)

DAY_LIST = []
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for i, day in enumerate(days):
    DAY_LIST.append((i+1, day))

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

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='openingHours')
    day = models.IntegerField(choices=DAY_LIST)
    from_hour = models.CharField(max_length=10, choices=TIME_LIST)
    to_hour = models.CharField(max_length=10, choices=TIME_LIST)
    is_closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Opening Hour'
        verbose_name_plural = "Opening Hour's"
        
        ordering = ('day',)
        unique_together = ('day', 'from_hour', 'to_hour')
    def __str__(self):
        return f"{self.get_day_display()}"
    