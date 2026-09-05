from django.urls import path
from .views import (
    CartSerializerListCreateAPIView,
    CartItemSerializerListCreateAPIView,
    OrderSerializerDetailAPIView,
    OrderItemSerializerListCreateAPIView,
    OrderStatusHistorySerializerListCreateAPIView,
    ReturnSerializerListCreateAPIView,
)


urlpatterns = [
    path(
        'cart-create-list',
        CartSerializerListCreateAPIView.as_view(),
        name='cart_list_create'
    ),
    path(
        'cart-item-create-list',
        CartItemSerializerListCreateAPIView.as_view(),
        name='cart_item_list_create'
    ),
    path(
        'order-detail',
        OrderSerializerDetailAPIView.as_view(),
        name='order_detail'
    ),
    path(
        'order-item-create-list',
        OrderItemSerializerListCreateAPIView.as_view(),
        name='order_item_list_create'
    ),
    path(
        'order-status-history-create-list',
        OrderStatusHistorySerializerListCreateAPIView.as_view(),
        name='order_status_history_list_create'
    ),
    path(
        'return-create-list',
        ReturnSerializerListCreateAPIView.as_view(),
        name='return_list_create'
    ),
]
