from rest_framework import serializers
from company_reports.models.company import CompanyData

class CompanyDataSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    has_logo = serializers.SerializerMethodField()

    class Meta:
        model = CompanyData
        fields = ['id', 'name', 'logo', 'logo_url', 'has_logo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'logo_url', 'has_logo']

    def get_logo_url(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url

    def get_has_logo(self, obj):
        return bool(obj.logo)
