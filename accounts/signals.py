from django.db.models.signals import post_save 
from django.dispatch import receiver

import uuid 
from django.contrib.auth import get_user_model
from vendor.models import Vendor
from customer.models import Customer
from helper.notification import send_account_activation_email

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    try:
        if created:
            if instance.is_customer:
                print("An Customer Profile Will Be Created.")
                Customer.objects.create(user=instance)
            elif instance.is_vendor:
                print("An Vendor Profile Will Be Created.")
                Vendor.objects.create(user=instance)
            else:
                print("User is an Admin")
                
            '''Sending Email code goes here'''
            email_token = str(uuid.uuid4())
            email = instance.email
            send_account_activation_email(email , email_token)
    except Exception as e:
        print(e)
