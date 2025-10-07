from django.contrib import admin
from ubi_geo.models.region import Region
from ubi_geo.models.province import Province
from ubi_geo.models.district import District

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "created_at")
    list_filter = ("country", "created_at", "deleted_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "created_at")
    list_filter = ("region", "created_at", "deleted_at")
    search_fields = ("name", "region__name")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province", "created_at")
    list_filter = ("province__region", "province", "created_at", "deleted_at")
    search_fields = ("name", "province__name", "province__region__name")
    readonly_fields = ("created_at", "updated_at", "deleted_at")