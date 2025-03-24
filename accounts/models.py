from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from helper.models import BaseModel
from django.utils.translation import gettext_lazy as gl
from location.models import Address
from cart.models import Cart, CartItem

# Create your models here.
class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is staff user')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser flag is false')
        
        return self._create_user(email, password, **extra_fields)

class User(BaseModel, AbstractUser, PermissionsMixin):
    username = None
    
    email = models.EmailField(gl('email address'), unique=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts'
    
    def __str__(self):
        return self.email
    
    def __unicode__(self):
        return self.id
    
    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_cart(self):
        cart, created = Cart.objects.get_or_create(customer=self)
        return cart
    
    def get_cart_item(self):
        cart = self.get_cart()
        return CartItem.objects.filter(cart=cart)
    
    def get_user_phone(self):
        phone = None
        if self.is_customer:
            phone = self.user_as_customer.phone
        if self.is_vendor:
            phone = self.user_as_vendor.phone
        if phone is not None:
            return phone
        else:
            return ""
    
    def get_user_address(self):
        address = Address.objects.filter(user_id=self.id).first()
        if address:
            return address.address
        else:
            return ""
        
    def get_coordinates(self):
        address = Address.objects.filter(user_id=self.id).first()
        if address:
            return [address.lat, address.long]
        else:
            return [0, 0]
    
    def get_user_profile_image(self):
        if self.is_customer:
            image_url = self.user_as_customer.image_url
            return image_url
        if self.is_vendor:
            image_url = self.user_as_vendor.image_url
            return image_url
