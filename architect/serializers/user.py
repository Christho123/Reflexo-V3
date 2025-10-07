from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # Campos de nombres de llaves foráneas
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    # Campo concatenado de nombre completo
    full_name = serializers.SerializerMethodField()
    
    # URL de la foto
    photo_url_display = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'document_type', 'document_type_name', 'document_number', 'photo_url', 'photo_url_display',
            'name', 'paternal_lastname', 'maternal_lastname', 'full_name', 'email', 'sex', 'phone', 'user_name',
            'password_change', 'last_session', 'account_statement', 'email_verified_at', 'country', 'country_name',
            'remember_token', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined',
            'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'deleted_at', 'last_login', 'date_joined',
            'document_type_name', 'country_name', 'full_name', 'photo_url_display'
        ]
    
    def get_full_name(self, obj):
        """Retorna el nombre completo concatenado."""
        parts = []
        if obj.name:
            parts.append(obj.name)
        if obj.paternal_lastname:
            parts.append(obj.paternal_lastname)
        if obj.maternal_lastname:
            parts.append(obj.maternal_lastname)
        return ' '.join(parts) if parts else ''
    
    def get_photo_url_display(self, obj):
        """Retorna la URL completa de la foto si existe."""
        if obj.photo_url:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo_url.url)
            return obj.photo_url.url
        return None