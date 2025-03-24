from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Cart
from .serializers import CartItemSerializer

class CartCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(customer=request.user)

        if cart:
            CART_VALUE_TOTAL = 0
            cart_items = [
                {
                    "food_item_id":item.food_item.id,
                    "cart_id":cart.id,
                    "cart_item_id":item.id,
                    "name":item.food_item.name, 
                    "image":item.food_item.image, 
                    "price":item.food_item.price,
                    "quantity":item.quantity,
                    "vendor":item.food_item.vendor.id,
                    "customer":request.user.id,
                    "restaurant":item.food_item.vendor.user_as_vendor.name,
                }
                
                for item in CartItem.objects.filter(cart=cart)
            ]
        else:
            cart_items = []
        return Response(cart_items, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(customer=request.user)
        
        # Create a cart item serializer instance with request data
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            # remember: we are checking with FoodItem id not cart id. 
            existing_item = CartItem.objects.filter(food_item_id=serializer.validated_data['food_item']).first()
            
            if existing_item:
                # Update the quantity if the item already exists
                existing_item.quantity = serializer.validated_data['quantity']
                existing_item.save()
            else:
                # Create a new cart item and associate it with the user's cart
                cart_item = serializer.save(cart=cart)
            
            cart_id = request.user.get_cart().id
            cart = CartItem.objects.filter(cart_id=cart_id)
            cart_items_data = [
                {
                    'food_item_id':item.food_item.id,
                    'cart_item_id': item.id,
                    'cart_id':cart_id,
                    "name":item.food_item.name, 
                    'image':item.food_item.image, 
                    'price':item.food_item.price,
                    'quantity': item.quantity,
                    "vendor":item.food_item.vendor.id,
                    "customer":request.user.id,
                    "restaurant":item.food_item.vendor.user_as_vendor.name,
                } 
                for item in cart
            ]   
            return Response(cart_items_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemRemoveView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        CartItem.objects.filter(id=pk).delete()

        cart_id = request.user.get_cart().id
        cart = CartItem.objects.filter(cart_id=cart_id)
        cart_items_data = [
            {
                'food_item_id':item.food_item.id,
                'cart_item_id': item.id,
                'cart_id':cart_id,
                "name":item.food_item.name, 
                'image':item.food_item.image, 
                'price':item.food_item.price,
                'quantity': item.quantity,
                "vendor":item.food_item.vendor.id,
                "customer":request.user.id,
                "restaurant":item.food_item.vendor.user_as_vendor.name,
            }
            for item in cart
        ]
        return Response(cart_items_data, status=status.HTTP_200_OK)