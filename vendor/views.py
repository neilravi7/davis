from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, OpeningHours
from .serializers import VendorSerializer, OpeningHoursSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated #IsAuthenticatedOrReadOnly,
from location.models import Address
from django.contrib.auth import get_user_model


class VendorListAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        vendors = Vendor.objects.filter(is_active=True)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

class VendorAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def get_object(self, user_id):
        try:
            return Vendor.objects.get(user__id=user_id)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        vendor = self.get_object(user_id)
        serializer = VendorSerializer(vendor)    
        return Response(serializer.data)

    def put(self, request, user_id):
        vendor = self.get_object(user_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()

            print(request.data)

            # Saving user.first_name and last_name.
            # This thing can be done with signal will be implemented
            vendor.is_active = request.data.get('is_active')
            vendor.image_url = request.data.get('image_url') 
            vendor.save()
            user = vendor.user
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.save()

            address_instance = Address.objects.get_or_create(user=user)[0]
            address_instance.address = request.data.get('address')
            address_instance.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        vendor = self.get_object(user_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


class TimingAPIView(APIView):
    permission_classes = (IsAuthenticated, )    
    def get(self, request):
        timing = OpeningHours.objects.filter(restaurant__id=request.user.user_as_vendor.id)
        serializer = OpeningHoursSerializer(timing, many=True)
        return Response(serializer.data)
    

class VendorProfileView(APIView):
    def get_object(self, user_id):
        try:
            return Vendor.objects.get(user__id=user_id)
        except Vendor.DoesNotExist:
            raise Http404
        
    def get(self, request, user_id):
        User = get_user_model()
        user = User.objects.get(id=user_id)
        vendor = self.get_object(user_id)

        vendor_name = vendor.name if vendor.name else ""
        image_url = vendor.image_url if vendor.image_url else ""
        cuisine_type = vendor.cuisine_type if vendor.cuisine_type else ""

        vendorData = {
            "name": vendor_name,
            "image": image_url,
            "ownerName": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "address": user.get_user_address(),
            "lat":user.get_coordinates()[0],
            "long":user.get_coordinates()[1],
            "openTime": "11:00 AM",
            "closeTime": "10:00 PM",
            "cuisineType":cuisine_type,
            "isAcceptingDeliveries": vendor.is_active,
        }

        return Response(vendorData, status=status.HTTP_200_OK)
    