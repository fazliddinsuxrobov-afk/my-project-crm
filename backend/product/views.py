from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from .models import Product, Category, ProductImage
from .serializer import ProductSerializer, CategorySerializer, ProductImageSerializer


@extend_schema(request=ProductSerializer, tags=['Products'])
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(request=CategorySerializer, tags=['Category'])
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(request=ProductImageSerializer, tags=['Product_images'])
class ProductImageListAPIView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer