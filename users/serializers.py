import email
from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=12)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = User 
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def validate(self, attrs):
        email = attrs.get("email", " ")
        username = attrs.get("username", " ")
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]
    
class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email"
        ]
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        
        return super().update(instance, validated_data)
        