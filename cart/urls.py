from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart API's
    path('items', views.CartCreateView().as_view(), name='cart'),
]