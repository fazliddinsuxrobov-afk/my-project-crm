from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, Return
from .serializer import (
    CartItemSerializer,
    CartSerializer,
    OrderItemSerializer,
    OrderSerializer,
    OrderStatusHistorySerializer,
    ReturnSerializer,
)


# Cart
@extend_schema(request=CartSerializer, tags=['Cart'])
class CartSerializerListCreateAPIView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


# CartItem
@extend_schema(request=CartItemSerializer, tags=['CartItem'])
class CartItemSerializerListCreateAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer





@extend_schema(request=OrderSerializer, tags=['Order'])
class OrderSerializerDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# OrderItem
@extend_schema(request=OrderItemSerializer, tags=['OrderItem'])
class OrderItemSerializerListCreateAPIView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# OrderStatusHistory
@extend_schema(request=OrderStatusHistorySerializer, tags=['OrderStatusHistory'])
class OrderStatusHistorySerializerListCreateAPIView(ListCreateAPIView):
    queryset = OrderStatusHistory.objects.all()
    serializer_class = OrderStatusHistorySerializer

# Return
@extend_schema(request=ReturnSerializer, tags=['Return'])
class ReturnSerializerListCreateAPIView(ListCreateAPIView):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer

