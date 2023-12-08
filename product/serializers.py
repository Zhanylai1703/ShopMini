from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from product.models import Product, Cart


class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'token',
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)

        return user

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'description',
            'price',
            'image',
        )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']


class CartGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']