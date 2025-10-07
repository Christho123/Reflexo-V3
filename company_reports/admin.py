from django.contrib import admin
from company_reports.models.company import CompanyData

@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('name', 'logo')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
