from django.urls import path
from .views import UsersListCreateAPIView, VerificationCodeListCreateAPIView

urlpatterns = [
    path('users-create-list', UsersListCreateAPIView.as_view(), name='user'),
    path('verificationcode-create-list', VerificationCodeListCreateAPIView.as_view(), name='code'),
]