from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('<uuid:user_id>/profile', views.CustomerAPIView().as_view(), name='customer_api'),
]