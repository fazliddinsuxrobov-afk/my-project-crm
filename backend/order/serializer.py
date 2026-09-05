from rest_framework.serializers import ModelSerializer

from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, Return

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderStatusHistorySerializer(ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = '__all__'

class ReturnSerializer(ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'