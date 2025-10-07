from rest_framework import serializers
from ubi_geo.models.region import Region


class RegionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Region"""
    
    class Meta:
        model = Region
        fields = ['id', 'name', 'country', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    
    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la región no puede estar vacío")
        return value.strip()
