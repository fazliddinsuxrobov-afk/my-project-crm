from rest_framework.serializers import ModelSerializer

from .models import User, VerificationCode


class SerializerUser(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SerializerVerificationCode(ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = '__all__'



