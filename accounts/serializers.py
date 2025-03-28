from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # user_type = serializers.CharField(write_only=True)

    # group =serializers.CharField()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password not match')
        return super().validate(data)
    
    
    def create(self, validated_data):        
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']

        user = self.Meta.model.objects.create_user(**data)

        user.save()

        return user
    
    class Meta:
        model = get_user_model()

        fields= (
            'id', 'email', 'password1', 'password2', 'first_name',
            'last_name', 'is_vendor', 'is_customer',
        )
        read_only_fields = ('id', 'password1', 'password2',)

   
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id' and key != 'first_name' and key != "last_name":
                token[key] = value
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data["userInfo"] = {
            "id":self.user.id,
            "name":self.user.get_full_name(),
            "email":self.user.email,
            "address":self.user.get_user_address(),
            "lat":self.user.get_coordinates()[0],
            "long":self.user.get_coordinates()[1],
            "phone":self.user.get_user_phone(),
            "profileImage":self.user.get_user_profile_image(),
            "role":{
                "isCustomer":self.user.is_customer,
                "isVendor":self.user.is_vendor
            }
        }
        
        # if self.user.is_customer:
        #     data["userInfo"]["cartItems"] = self.user.get_cart_item()
        
        data["success"] = True
        return data

User = get_user_model()

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        read_only_fields = ('id', 'email',)

    def update(self, instance, validated_data):
        # Exclude password fields from validated data
        validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        
        # Perform the usual update logic
        instance = super().update(instance, validated_data)
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ( 'old_password', 'password', 'password2')

    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'password did not match'})
            
        return super().validate(attrs)
    
    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is not correct'})

        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance