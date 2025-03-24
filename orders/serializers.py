from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', "total_amount", "status", "display_id" , "stripe_checkout_id", "payment_status", "firebase_order_id")
        read_only_fields = ('id',)
        depth = 1