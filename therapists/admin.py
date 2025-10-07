from django.contrib import admin
from therapists.models.therapist import Therapist

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name_paternal", "document_number", "region", "province", "district", "deleted_at")
    list_filter = ("region", "province", "district", "created_at", "deleted_at")
    search_fields = ("first_name", "last_name_paternal", "last_name_maternal", "document_number")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
