from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema

from .models import User, VerificationCode
from .serializer import SerializerUser, SerializerVerificationCode


@extend_schema(request=SerializerUser, tags=['Users'])
class UsersListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SerializerUser

@extend_schema(request=SerializerVerificationCode, tags=['VerificationCode'])
class VerificationCodeListCreateAPIView(ListCreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = SerializerVerificationCode

