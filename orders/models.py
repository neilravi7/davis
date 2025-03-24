from django.db import models
from helper.models import BaseModel
from django.conf import settings
from menu.models import FoodItem

# Create your models here.

class Order(BaseModel, models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
    )

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='order_as_vendor'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='order_as_customer'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    display_id = models.CharField(max_length=10)
    stripe_checkout_id = models.CharField(max_length=80, null=True, blank=True)
    payment_status=models.CharField(max_length=80, null=True, blank=True)
    firebase_order_id=models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'orders'

    def get_restaurant_name(self):
        return self.vendor.user_as_vendor.name

    def get_order_items(self):
        return OrderItem.objects.filter(order_id=self.id)
    
    def get_serialize_items(self):
        items = self.get_order_items()
        if len(items) == 0:
            return []
        else:
            return [
            {
                "id":item.id, 
                "name":item.food_item.name, 
                "image":item.food_item.image,
                "price":(item.food_item.price)/100,
                "quantity":item.quantity
            } 
                for item in items
            ]
    
    def get_order_total(self):
        sub_total = 0
        TAX_PERCENTAGE=4
        DELIVERY = 5

        for item in self.get_order_items():
            sub_total += item.food_item.price * item.quantity
        
        tax = (sub_total*TAX_PERCENTAGE)/100
        TOTAL  = sub_total+tax+DELIVERY 

        return {
            "sub_total": TOTAL, 
            "breakdown":{
                "sub_total":sub_total,
                "tax_charges":tax,
                "delivery_charges":DELIVERY,
                "display_total":TOTAL/100
            }
        }
    
    def get_firebase_order_id(self):
        return self.firebase_order_id
    

class OrderItem(BaseModel, models.Model):
    order = models.ForeignKey(
        Order,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    food_item = models.ForeignKey(
        FoodItem,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'