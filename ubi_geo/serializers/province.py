from rest_framework import serializers
from ubi_geo.models.province import Province


class ProvinceSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Province"""
    
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'name', 'region', 'region_name', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'region_name', 'created_at', 'updated_at', 'deleted_at']
    
    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la provincia no puede estar vacío")
        return value.strip()
    
    def validate_region(self, value):
        """Validar que la región exista"""
        if not value:
            raise serializers.ValidationError("Debe seleccionar una región")
        return value
