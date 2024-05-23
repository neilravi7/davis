from django.db import models
from django.conf import settings
from helper.models import BaseModel
import geocoder

# Create your models here.
class Address(BaseModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "address"
    
    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=settings.MAPBOX_KEY)
        self.lat = g.lat
        self.long = g.lng
        return super(Address, self).save(*args, **kwargs)



