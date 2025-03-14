from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from helper.models import BaseModel

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
# Create your models here.

class Vendor(BaseModel, models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='user_as_vendor'
    )
    image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    cuisine_type = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    rating = models.IntegerField(default=1, null=True, blank=True)  

    class Meta:
        db_table = "vendors"

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        # self.image_url = "https://delishnow.s3.us-east-005.backblazeb2.com/hero-1.jpg" # amazon bucket will take place here.
        return super(Vendor, self).save(*args, **kwargs)
    

class Day(models.TextChoices):
    MONDAY = 'mon', _('Monday')
    TUESDAY = 'tue', _('Tuesday')
    WEDNESDAY = 'wed', _('Wednesday')
    THURSDAY = 'thu', _('Thursday')
    FRIDAY = 'fri', _('Friday')
    SATURDAY = 'sat', _('Saturday')
    SUNDAY = 'sun', _('Sunday')

class OpeningHours(BaseModel, models.Model):
    restaurant = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="opening_hours")
    day = models.CharField(max_length=5, choices=Day.choices)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        db_table = "opening_hours"
        unique_together = ('restaurant', 'day')
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_display()}"
    
    def clean(self) -> None:
        if self.opening_time >= self.closing_time:
            raise ValidationError("Invalid timing, Opening time must be before closing time.")