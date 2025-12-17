from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser,FarmerProfile,BuyerProfile,ProductListing

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'is_active',
        ]
        read_only_fields = ['id', 'is_active']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone_number',
            'password',
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled!")
            else:
                raise serializers.ValidationError("Invalid login credentials!")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data

class FarmerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile

        fields = [
            'farm_name',
            'farm_location',
            'farm_size',
            'farm_image',
            'farm_description',
        ]

class FarmerProfilesListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FarmerProfile

        fields = [
            'id',
            'farm_name',
            'farm_location',
            'farm_size',
            'farm_image',
            'farm_description',
            'created_at',
            'updated_at',
        ]
class FarmerProfileDetailsSerializer(serializers.ModelSerializer):
    
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile

        fields = [
            'id',
            'user',
            'farm_name',
            'farm_location',
            'farm_size',
            'farm_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user']

class BuyerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile

        fields = [
            'company_name',
            'company_address',
            'company_description',
            'company_image',
        ]

class BuyerProfilesListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BuyerProfile

        fields = [
            'id',
            'company_name',
            'company_address',
            'company_image',
            'company_description',
            'created_at',
            'updated_at',
        ]
class BuyerProfileDetailsSerializer(serializers.ModelSerializer):
    
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = BuyerProfile

        fields = [
            'id',
            'user',
            'company_name',
            'company_address',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing

        fields = [
            'product_name',
            'quantity',
            'price_per_unit',
            'description',
            'product_image',
        ]
class ProductDetailsSerializer(serializers.ModelSerializer):

    farmer = FarmerProfileDetailsSerializer(read_only=True)
    class Meta:
        model = ProductListing

        fields = [
            'id',
            'farmer',
            'product_name',
            'quantity',
            'price_per_unit',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'farmer']

class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductListing

        fields = [
            'id',
            'product_name',
            'quantity',
            'price_per_unit',
            'description',
            'product_image',
            'created_at',
            'updated_at',
        ]
