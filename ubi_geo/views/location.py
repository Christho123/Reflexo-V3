from rest_framework.viewsets import ReadOnlyModelViewSet
from ubi_geo.models.region import Region
from ubi_geo.models.province import Province
from ubi_geo.models.district import District
from ubi_geo.serializers.region import RegionSerializer
from ubi_geo.serializers.province import ProvinceSerializer
from ubi_geo.serializers.district import DistrictSerializer

class RegionViewSet(ReadOnlyModelViewSet):
    queryset = Region.objects.filter(deleted_at__isnull=True).order_by("name")
    serializer_class = RegionSerializer

class ProvinceViewSet(ReadOnlyModelViewSet):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        qs = Province.objects.select_related("region").filter(deleted_at__isnull=True).order_by("name")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs

class DistrictViewSet(ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        qs = District.objects.select_related("province", "province__region").filter(deleted_at__isnull=True).order_by("name")
        province_id = self.request.query_params.get("province")
        if province_id:
            qs = qs.filter(province_id=province_id)
        return qs
