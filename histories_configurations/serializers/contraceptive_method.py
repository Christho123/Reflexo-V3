from rest_framework import serializers
from ..models.contraceptive_method import ContraceptiveMethod


class ContraceptiveMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContraceptiveMethod
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]



