from rest_framework import serializers
from ubi_geo.models.region import Region
from ubi_geo.models.province import Province
from ubi_geo.models.district import District

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "name", "country", "created_at", "updated_at", "deleted_at")

class ProvinceSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Province
        fields = ("id", "name", "region", "created_at", "updated_at", "deleted_at")

class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = District
        fields = ("id", "name", "province", "created_at", "updated_at", "deleted_at")
