from rest_framework.authtoken.models import Token
# from .tokens import create_jwt_pair_for_user
from .models import User
from .models import CustomUser
from rest_framework import serializers
from user_profile.models import OwnerProfile
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User1=get_user_model()
    

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerProfile
        exclude= 'user',

class OwnerRegisterSerializer(serializers.ModelSerializer):
    profile = OwnerSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_owner(**validated_data)
        OwnerProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            # age=profile_data['age'],
            gender=profile_data['gender']
        )
        Token.objects.create(user=user)

        return user
    def get_attribute(self, instance):
        return super().get_attribute(instance)
    
    
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields =['email', 'password']

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=User1
        fields=["email","password"]        