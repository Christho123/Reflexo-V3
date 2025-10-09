from rest_framework import serializers
from ..models.diu_type import DIUType

class DIUTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DIUType
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]




