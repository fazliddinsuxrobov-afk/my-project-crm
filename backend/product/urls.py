from django.urls import path

from .views import ProductListAPIView, ProductImageListAPIView, CategoryListAPIView

urlpatterns = [
    path('product-list', ProductListAPIView.as_view(), name='product_list' ),
    path('product-image-list', ProductImageListAPIView.as_view(), name='product_image' ),
    
    path('category-list', CategoryListAPIView.as_view(), name='category_list' ),
]