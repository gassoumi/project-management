from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# User Serialize
class UserSerializer(serializers.ModelSerializer):
    userProfile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'userProfile')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('email', None) is not None:
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
        else:
            user = User(
                username=validated_data['username']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_superuser:
            return user
        raise serializers.ValidationError(
            {"username or password": "Incorrect credentials"})
