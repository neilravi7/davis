from rest_framework import serializers
from .models import Vendor, OpeningHours
from django.contrib.auth import get_user_model

class VendorSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    lat = serializers.SerializerMethodField()
    long = serializers.SerializerMethodField()


    class Meta:
        model = Vendor
        fields = (
            'first_name', 'last_name', 'email', 'image_url', 'name', 'phone', 'cuisine_type',
            'description', 'id', 'user', 'is_active', 'address', 'rating', 'discount', "lat", "long",
        )
        read_only_fields = ('id', 'email', 'is_approved', 'is_active')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else ""

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else ""
    
    def get_email(self, obj):
        return obj.user.email if obj.user else ""
    
    def get_address(self, obj):
        return obj.user.get_user_address() if obj.user else ""

    def get_lat(self, obj):
        return obj.user.get_coordinates()[0] if obj.user else ""
    
    def get_long(self, obj):
        return obj.user.get_coordinates()[1] if obj.user else ""

    

class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = (
            'id', 'day', 'opening_time', 'closing_time',
        )
        read_only_fields = ('id',)