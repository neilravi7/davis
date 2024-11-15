from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('list', views.VendorListAPIView().as_view(), name='vendor_list_api'),
    path('<uuid:user_id>/profile', views.VendorAPIView().as_view(), name='vendor_api'),
    path('opening/hours', views.TimingAPIView().as_view(), name='vendor_timing'),
]