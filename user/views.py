from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, UserCreateSerializer
from user.models import OTP
from utils.functions import generate_verification_code, send_sms_verification


User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and send verification code via SMS
        verification_code = generate_verification_code()
        send_sms_verification(user.phone, verification_code)
        OTP.objects.create(user, verification_code).save()

        headers = self.get_success_headers(user)
        return Response(
            {"message": "User created successfully. Check sms for verification code."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserVerifyCodeAPIView(generics.CreateAPIView):
    pass


class UserMeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
