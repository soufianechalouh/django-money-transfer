from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password"]

    def validate(self, attrs):
        username = attrs.get("username", "")

        if not str(username).isalnum():
            raise serializers.ValidationError("username should be alphanumeric")
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailValidationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return user.tokens()

    class Meta:
        model = User
        fields = ["email", "password", "username", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")

        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")
        return {
            "email": user.email,
            "username": user.username,
            "token": user.tokens,
        }
