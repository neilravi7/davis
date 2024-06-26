from django.db import models
from django.conf import settings
from helper.models import BaseModel
# Create your models here.

class Customer(BaseModel, models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='user_as_customer',
    )
    image_url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        db_table='customers'
    
    def save(self, *args, **kwargs):
        self.image_url = "http://placebeard.it/640x480"
        return super(Customer, self).save(*args, **kwargs)
