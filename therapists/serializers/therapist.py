import re
from datetime import date
from rest_framework import serializers
from therapists.models import Therapist 
from ubi_geo.models import Region, Province, District
from ubi_geo.serializers import RegionSerializer, ProvinceSerializer, DistrictSerializer
from histories_configurations.models import DocumentType
from histories_configurations.serializers import DocumentTypeSerializer
from architect.models import Role
from architect.serializers import RoleSerializer

class TherapistSerializer(serializers.ModelSerializer):
    # Serializadores anidados para mostrar datos completos
    region = RegionSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    document_type = DocumentTypeSerializer(read_only=True)  # Para lectura
    full_name = serializers.SerializerMethodField()
    
    # Campos de nombres para mostrar en lugar de IDs
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    # Hago document_number opcional y permito blancos
    document_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Campos para escritura (crear/actualizar)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), 
        source='region', 
        write_only=True
    )
    province_id = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(), 
        source='province', 
        write_only=True
    )
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), 
        source='district', 
        write_only=True
    )
    document_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(),
        source='document_type',
        write_only=True,
        error_messages={
            'does_not_exist': 'El tipo de documento seleccionado no existe.'
        }
    )

    class Meta:
        model = Therapist
        fields = [
            'id',
            'document_type',
            'document_type_name',
            'document_number',
            'license_number',
            'last_name_paternal',
            'last_name_maternal',
            'first_name',
            'full_name',
            'birth_date',
            'gender',
            'personal_reference',
            'is_active',
            'phone',
            'email',
            'region',
            'region_name',
            'province',
            'province_name',
            'district',
            'district_name',
            'address',
            'profile_picture',
            'created_at',
            'updated_at',
            'deleted_at',
            'region_id',
            'province_id',
            'district_id',
            'document_type_id',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
        
    def validate(self, attrs):
        """
        Asegura coherencia jerárquica:
        province debe pertenecer a region
        district debe pertenecer a province
        """
        region = attrs.get("region") or getattr(self.instance, "region", None)
        province = attrs.get("province") or getattr(self.instance, "province", None)
        district = attrs.get("district") or getattr(self.instance, "district", None)

        if province and region and province.region_id != region.id:
            raise serializers.ValidationError(
                "La provincia seleccionada no pertenece a la región."
            )
        if district and province and district.province_id != province.id:
            raise serializers.ValidationError(
                "El distrito seleccionado no pertenece a la provincia."
            )
        return attrs

    def validate_document_number(self, value):
        # Si el valor es nulo o vacío, no se aplica validación
        if not value:
            return value

        # Obtener el tipo de documento desde los datos iniciales o la instancia
        doc_type_id = self.initial_data.get("document_type_id")
        
        # Si no está en initial_data, intentar obtener de la instancia existente
        if not doc_type_id and self.instance:
            doc_type_id = self.instance.document_type_id
        
        if not doc_type_id:
            return value  # No podemos validar sin tipo de documento
        
        # Obtener el nombre del tipo de documento para las validaciones
        try:
            document_type = DocumentType.objects.get(id=doc_type_id)
            doc_type_name = document_type.name.upper()
        except DocumentType.DoesNotExist:
            # La validación de existencia se hará en document_type_id field
            return value

        # Validaciones según el tipo de documento
        if doc_type_name == "DNI":
            if not value.isdigit():
                raise serializers.ValidationError("El DNI debe contener solo números.")
            if not (8 <= len(value) <= 9):
                raise serializers.ValidationError(
                    "El DNI debe tener entre 8 y 9 dígitos."
                )

        elif doc_type_name == "CE" or "CARNE DE EXTRANJERIA" in doc_type_name:
            if not value.isdigit():
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe contener solo números."
                )
            if len(value) > 12:
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe tener máximo 12 dígitos."
                )

        elif doc_type_name == "PTP":
            if not value.isdigit():
                raise serializers.ValidationError("El PTP debe contener solo números.")
            if len(value) != 9:
                raise serializers.ValidationError(
                    "El PTP debe tener exactamente 9 dígitos."
                )

        elif doc_type_name == "CR" or "CARNE DE REFUGIADO" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Carné de Refugiado debe contener solo letras y números."
                )

        elif doc_type_name == "PAS" or "PASAPORTE" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Pasaporte debe contener solo letras y números."
                )

        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_last_name_paternal(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido paterno no puede estar vacío.")
        return value

    def validate_last_name_maternal(self, value):
        # Este campo puede ser null/blank, pero si tiene valor debe ser válido
        if value and not value.strip():
            raise serializers.ValidationError("El apellido materno no puede estar vacío.")
        return value

    def validate_personal_reference(self, value):
        if value and not re.match(r"^[A-Za-z0-9\s]+$", value):
            raise serializers.ValidationError(
                "La referencia personal solo puede contener letras y números."
            )
        return value

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo dígitos.")
        if value and len(value) > 20:
            raise serializers.ValidationError(
                "El teléfono debe tener máximo 20 dígitos."
            )
        return value

    def validate_email(self, value):
        if value:
            pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("El correo debe ser válido y terminar en @gmail.com (ejemplo: usuario@gmail.com).")
        return value

    def validate_birth_date(self, value):
        if value:
            today = date.today()

            # No permitir fechas futuras
            if value.date() > today:
                raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")

            # Calcular edad
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise serializers.ValidationError("El terapeuta debe tener al menos 18 años.")

        return value

    def validate_profile_picture(self, value):
        if not value:
            return value
        # Validar que sea una cadena válida (URL o path)
        if not isinstance(value, str):
            raise serializers.ValidationError(
                "La imagen debe ser una URL válida."
            )
        return value
    
    def get_full_name(self, obj):
        """Concatena first_name + last_name_paternal + last_name_maternal"""
        full_name_parts = []
        
        if obj.first_name:
            full_name_parts.append(obj.first_name)
        if obj.last_name_paternal:
            full_name_parts.append(obj.last_name_paternal)
        if obj.last_name_maternal:
            full_name_parts.append(obj.last_name_maternal)
            
        return ' '.join(full_name_parts) if full_name_parts else ''