from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.region import RegionViewSet
from .views.province import ProvinceViewSet
from .views.district import DistrictViewSet

router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"provinces", ProvinceViewSet, basename="province")
router.register(r"districts", DistrictViewSet, basename="district")

urlpatterns = [
    path('', include(router.urls)),  # APIs disponibles en la raíz
]