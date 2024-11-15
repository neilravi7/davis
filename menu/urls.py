from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Categories API's
    path('category/list', views.CategoryAPIView().as_view(), name='category_list'),
    path('category/create', views.CategoryCreateView().as_view(), name='category_create'),
    path('<uuid:pk>/category', views.CategoryAPIView().as_view(), name='category'),
    
    # Food items API's
    path('food/item/list', views.FoodItemListView().as_view(), name='food_item_list'),
    path('food/<uuid:pk>/items', views.FoodItemCustomerAPIView().as_view(), name='food_item_list_customer'),
    path('food/item/create', views.FoodItemCreateView().as_view(), name='food_item_create'),
    path('food/item/<uuid:pk>', views.FoodItemAPIView().as_view(), name='food_item'),
]