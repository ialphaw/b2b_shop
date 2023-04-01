from rest_framework import serializers

from shop.models import Charge


class ChargeSerializer(serializers.ModelSerializer):
    """Serializer for the Charge model."""
    
    class Meta:
        model = Charge
        fields = "__all__"
