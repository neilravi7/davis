# django core imports
from django.contrib.auth import get_user_model

# rest_framework imports
from rest_framework import generics
from rest_framework.views import APIView

# Token Views (Authentication)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

# File Upload API's
from rest_framework.parsers import MultiPartParser, FormParser
import uuid
# from b2sdk.v2 import InMemoryAccountInfo, B2Api
from django.conf import settings
import requests


# serializers imports
from . import serializers


# Auth API's
class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


# Players API's
class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'


class UserDelete(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    lookup_field = 'pk'


class UserPartialUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'

 
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response({"message":"user logout"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message":str(e)} , status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


# class DirectB2UploadAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get("file")  # Get the file from the request
#         source = request.POST.get("source")
        
#         if not file_obj:
#             return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
#         file_name = file_obj.name.split(".")[1]

#         # Generate a unique filename
#         unique_filename = f"{source}/so_{uuid.uuid4().hex}.{file_name}"

#         print(settings.B2_KEY_ID, settings.B2_APPLICATION_KEY, settings.B2_BUCKET_NAME)

#         try:
#             # Initialize Backblaze B2 API
#             info = InMemoryAccountInfo()
#             b2_api = B2Api(info)
#             b2_api.authorize_account("production", settings.B2_KEY_ID, settings.B2_APPLICATION_KEY)

#             # Get the bucket
#             bucket = b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

#             # Upload the file
#             bucket.upload_bytes(file_obj.read(), unique_filename)

#             # Construct the file URL
#             file_url = f"https://f002.backblazeb2.com/file/{settings.B2_BUCKET_NAME}/{unique_filename}"

#             return Response({"message": "Upload successful", "file_url": file_url}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        album_id = request.POST.get('album')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        
        url = f"https://api.imgbb.com/1/upload?key={settings.IMGBB_API_KEY}"
        
        files = {"image": file}
        data = {}

        if album_id:
            data['album'] = album_id
        
        response = requests.post(url, files=files, data=data)
        
        data = response.json()
        
        if response.status_code == 200:
            return Response({"url": data["data"]["url"]}, status=201)
        else:
            return Response({"error": data}, status=response.status_code)