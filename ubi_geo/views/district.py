# -*- coding: utf-8 -*-
from rest_framework.viewsets import ReadOnlyModelViewSet
from ubi_geo.models.district import District
from ubi_geo.serializers.district import DistrictSerializer


class DistrictViewSet(ReadOnlyModelViewSet):
    """
    GET /api/districts/                  -> lista (se puede filtrar)
    GET /api/districts/{id}/             -> detalle

    Filtros por querystring:
      - ?province=<id>           -> distritos de esa provincia
    """
    serializer_class = DistrictSerializer

    def get_queryset(self):
        qs = (
            District.objects
            .select_related("province", "province__region")
            .filter(deleted_at__isnull=True)
            .order_by("name")
        )
        province_id = self.request.query_params.get("province")
        if province_id:
            qs = qs.filter(province_id=province_id)
        return qs
