from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, FoodItem
from .serializers import CategorySerializer, FoodItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


# Permission
from rest_framework.permissions import IsAuthenticated #IsAuthenticatedOrReadOnly,

class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(vendor=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FoodItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        available = request.query_params.get("available")
        if available is not None:
            if available.lower() == "true":
                available = True
            elif available.lower() == "false":
                available = False
            else:
                raise ValidationError({"available": "Invalid value. Must be 'true' or 'false'."})
            
            food_items = []
            food_items = FoodItem.objects.filter(vendor_id=request.user.id, is_available=available)
        else:
            food_items = FoodItem.objects.filter(vendor_id=request.user.id)
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)
    

class FoodItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        food_item = get_object_or_404(FoodItem, pk=pk)
        serializer = FoodItemSerializer(food_item)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        food_item = get_object_or_404(FoodItem, pk=pk)
        category = get_object_or_404(Category, pk=request.data.get('category'))
        serializer = FoodItemSerializer(food_item, data=request.data)
        if serializer.is_valid():
            food_item.category = category
            serializer.save()
            food_item.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        food_item = get_object_or_404(FoodItem, pk=pk)
        serializer = FoodItemSerializer(food_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        food_item = get_object_or_404(FoodItem, pk=pk)
        food_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FoodItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user, category_id=request.data.get('category'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FoodItemCustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        food_items = FoodItem.objects.filter(vendor_id=pk, is_available=True)
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)