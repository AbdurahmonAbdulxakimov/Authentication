from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": _("Passwords don't match.")}
            )
        attrs.pop("password_confirmation", None)
        return super().validate(attrs)

    def create(self, validated_data):
        model = self.Meta.model
        user = model.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, source="get_full_name")

    class Meta:
        model = User
        fields = [
            "phone",
            "full_name",
        ]


class UserVerifyCodeSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(min_value=100000, max_value=999999)

    class Meta:
        model = User
        fields = ["phone", "code"]

    def create(self, validated_data):
        user = self.Meta.model.objects.get(phone=validated_data["phone"])
        if validated_data["code"] == user.otps[-1].code:
            user.is_active = True
            user.save()
            return user
        raise serializers.ValidationError("Code is not valid!")
