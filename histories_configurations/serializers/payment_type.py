from rest_framework import serializers
from ..models import PaymentType

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ["id", "name", "description", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
