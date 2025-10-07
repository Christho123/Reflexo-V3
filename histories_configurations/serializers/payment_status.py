from rest_framework import serializers
from ..models import PaymentStatus

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
