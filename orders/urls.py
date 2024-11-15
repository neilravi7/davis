from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('list', views.OrderListAPIView().as_view(), name='orders'),
]