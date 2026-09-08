from django.urls import path
from .views import (
    CartSerializerListCreateAPIView, CartItemSerializerListCreateAPIView,
    OrderSerializerDetailAPIView, OrderItemSerializerListCreateAPIView,
    OrderStatusHistorySerializerListCreateAPIView, ReturnSerializerListCreateAPIView,
)


urlpatterns = [
    path('cart/', CartSerializerListCreateAPIView.as_view(), name='cart-list-create'),
    path('cart-items/', CartItemSerializerListCreateAPIView.as_view(), name='cart-item-list-create'),

    path('orders/<int:pk>/', OrderSerializerDetailAPIView.as_view(), name='order-detail'),
    path('order-items/', OrderItemSerializerListCreateAPIView.as_view(), name='order-item-list-create'),
    path('order-status-history/', OrderStatusHistorySerializerListCreateAPIView.as_view(), name='order-status-history-list-create'),
    
    path('returns/', ReturnSerializerListCreateAPIView.as_view(), name='return-list-create'),
]
