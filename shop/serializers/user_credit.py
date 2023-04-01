from rest_framework import serializers

from shop.models import UserCredit
from shop.serializers import UserSerializer


class UserCreditSerializer(serializers.ModelSerializer):
    """Serializer for the UserCredit model."""

    class Meta:
        model = UserCredit
        fields = "__all__"
        read_only_fields = ("user", "credit")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response
