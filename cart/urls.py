from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart API's
    path('items', views.CartCreateView().as_view(), name='cart_item_create_and_update'),
    path('items/<uuid:pk>/remove', views.CartItemRemoveView().as_view(), name="cart_item_remove"),

]