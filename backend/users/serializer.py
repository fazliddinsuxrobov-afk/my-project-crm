from rest_framework.serializers import ModelSerializer

from .models import User, UserManager, VerificationCode


class SerializerUser(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SerializerUserManager(ModelSerializer):
    class Meta:
        model = UserManager
        fields = '__all__'


class SerializerVerificationCode(ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = '__all__'



