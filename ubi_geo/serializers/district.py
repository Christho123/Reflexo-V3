from rest_framework import serializers
from ubi_geo.models.district import District


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer para el modelo District"""
    
    province_name = serializers.CharField(source='province.name', read_only=True)
    region_name = serializers.CharField(source='province.region.name', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'name', 'province', 'province_name', 'region_name', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'province_name', 'region_name', 'created_at', 'updated_at', 'deleted_at']
    
    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del distrito no puede estar vacío")
        return value.strip()
    
    def validate_province(self, value):
        """Validar que la provincia exista"""
        if not value:
            raise serializers.ValidationError("Debe seleccionar una provincia")
        return value
