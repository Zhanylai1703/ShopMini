from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from product.serializers import ProductSerializer, CartSerializer, CartGetSerializer
from product.models import Product, Cart


class ProductViewSet(viewsets.ModelViewSet):
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
    