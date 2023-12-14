from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from product.serializers import ProductSerializer, CartSerializer, CartGetSerializer, RegistrationSerializer, \
    LoginSerializer
from product.models import Product, Cart


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetAllProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class AddToCartView(views.APIView):
    @swagger_auto_schema(request_body=CartSerializer)
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        user = request.user

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        cart_item.quantity += quantity
        cart_item.save()

        return Response({'message': 'Product added to cart successfully'})


class ViewCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartGetSerializer(cart_items, many=True)
        return Response({'cart': serializer.data})


class RemoveFromCartView(views.APIView):
    def delete(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, pk=product_id)

        try:
            cart_item = Cart.objects.get(user=user, product=product)

            cart_item.delete()

            return Response({'message': 'Product removed from cart successfully'})
        except Cart.DoesNotExist:
            return Response({'message': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(views.APIView):
    def delete(self, request):
        user = request.user

        try:
            cart_items = Cart.objects.filter(user=user)
            cart_items.delete()

            return Response({'message': 'Cart cleared successfully'})
        except Cart.DoesNotExist:
            return Response({'message': 'Cart is already empty'}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
