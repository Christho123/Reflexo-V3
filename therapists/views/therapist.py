# -*- coding: utf-8 -*-
"""
Vistas para la aplicación de terapeutas.
Maneja las operaciones CRUD y renderizado de templates.
"""

from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from therapists.models.therapist import Therapist
from therapists.serializers.therapist import TherapistSerializer


class TherapistViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de terapeutas.
    Incluye:
      - Filtros por estado y por región/provincia/distrito (IDs).
      - Búsqueda por campos.
      - Soft delete y restauración.
      - Solo PUT para edición (con edición parcial).
    """
    serializer_class = TherapistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "first_name",
        "last_name_paternal",
        "last_name_maternal",
        "license_number",
        "document_number",
        "document_type__name",
        "email",
        "phone",
        "address",
        # búsqueda por nombres de ubicaciones (FK)
        "region__name",
        "province__name",
        "district__name",
    ]

    def get_queryset(self):
        """
        - Usa select_related para evitar N+1 en las FKs de ubicación.
        - Filtra por activo/inactivo (param 'active').
        - Filtra opcionalmente por IDs de region/province/district.
        """
        qs = (
            Therapist.objects.select_related("region", "province", "district")
            .all()
        )

        # filtro por estado (activo por defecto)
        active = self.request.query_params.get("active", "true").lower()
        if active in ("true", "1", "yes"):
            qs = qs.filter(deleted_at__isnull=True)
        elif active in ("false", "0", "no"):
            qs = qs.filter(deleted_at__isnull=False)

        # filtros por ubicación (IDs)
        region = self.request.query_params.get("region")
        province = self.request.query_params.get("province")
        district = self.request.query_params.get("district")
        if region:
            qs = qs.filter(region_id=region)
        if province:
            qs = qs.filter(province_id=province)
        if district:
            qs = qs.filter(district_id=district)

        return qs

    def update(self, request, *args, **kwargs):
        """
        PUT con edición parcial - permite editar cualquier campo sin requerir todos.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error al actualizar el terapeuta: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete - marca como inactivo en lugar de eliminar.
        """
        try:
            instance = self.get_object()
            if instance.deleted_at is not None:
                return Response({'error': 'El terapeuta ya está inactivo'}, status=status.HTTP_400_BAD_REQUEST)
            
            instance.soft_delete()
            return Response({
                'message': 'Terapeuta marcado como inactivo exitosamente',
                'id': instance.id,
                'name': instance.get_full_name(),
                'deleted_at': instance.deleted_at.isoformat() if instance.deleted_at else None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al eliminar el terapeuta: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"])
    def inactive(self, request):
        """
        Endpoint para obtener terapeutas inactivos.
        Respeta paginación y serializer.
        """
        queryset = self.get_queryset().filter(deleted_at__isnull=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        """
        Restaura un terapeuta marcándolo como activo.
        """
        try:
            therapist = Therapist.objects.get(pk=pk, deleted_at__isnull=False)
            therapist.restore()
            return Response({
                'message': 'Terapeuta restaurado exitosamente',
                'id': therapist.id,
                'name': therapist.get_full_name(),
                'is_active': therapist.is_active,
                'restored_at': therapist.updated_at.isoformat()
            }, status=status.HTTP_200_OK)
        except Therapist.DoesNotExist:
            return Response({"error": "Terapeuta inactivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al restaurar el terapeuta: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post", "put", "patch", "delete"])
    def upload_photo(self, request, pk=None):
        """
        Maneja las operaciones de foto de perfil del terapeuta.
        - POST: Sube nueva foto
        - PUT: Actualiza/reemplaza foto existente
        - PATCH: Actualización parcial (igual que PUT)
        - DELETE: Elimina foto existente
        """
        try:
            therapist = self.get_object()
            
            if request.method == "POST":
                return self._upload_new_photo(therapist, request)
            elif request.method in ["PUT", "PATCH"]:
                return self._update_photo(therapist, request)
            elif request.method == "DELETE":
                return self._delete_photo(therapist, request)
                
        except Exception as e:
            return Response({'error': f'Error al procesar la foto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _upload_new_photo(self, therapist, request):
        """
        Sube una nueva foto de perfil para el terapeuta.
        """
        if 'profile_picture' not in request.FILES:
            return Response({'error': 'No se proporcionó archivo de imagen'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar archivo
        validation_error = self._validate_image(request.FILES['profile_picture'])
        if validation_error:
            return validation_error
        
        # Guardar la imagen
        therapist.profile_picture = request.FILES['profile_picture']
        therapist.save(update_fields=['profile_picture'])
        
        return Response({
            'message': 'Foto de perfil subida exitosamente',
            'id': therapist.id,
            'name': therapist.get_full_name(),
            'profile_picture_url': therapist.get_profile_picture_url(),
            'uploaded_at': therapist.updated_at.isoformat()
        }, status=status.HTTP_201_CREATED)
    
    def _update_photo(self, therapist, request):
        """
        Actualiza/reemplaza la foto de perfil del terapeuta.
        """
        if 'profile_picture' not in request.FILES:
            return Response({'error': 'No se proporcionó archivo de imagen'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar archivo
        validation_error = self._validate_image(request.FILES['profile_picture'])
        if validation_error:
            return validation_error
        
        # Eliminar foto anterior si existe
        if therapist.profile_picture:
            try:
                therapist.profile_picture.delete(save=False)
            except:
                pass  # Si no se puede eliminar, continuar
        
        # Guardar la nueva imagen
        therapist.profile_picture = request.FILES['profile_picture']
        therapist.save(update_fields=['profile_picture'])
        
        return Response({
            'message': 'Foto de perfil actualizada exitosamente',
            'id': therapist.id,
            'name': therapist.get_full_name(),
            'profile_picture_url': therapist.get_profile_picture_url(),
            'updated_at': therapist.updated_at.isoformat()
        }, status=status.HTTP_200_OK)
    
    def _delete_photo(self, therapist, request):
        """
        Elimina la foto de perfil del terapeuta.
        """
        if not therapist.profile_picture:
            return Response({'error': 'El terapeuta no tiene foto de perfil'}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminar la foto
        therapist.profile_picture.delete(save=False)
        therapist.profile_picture = None
        therapist.save(update_fields=['profile_picture'])
        
        return Response({
            'message': 'Foto de perfil eliminada exitosamente',
            'id': therapist.id,
            'name': therapist.get_full_name(),
            'profile_picture_url': None,
            'deleted_at': therapist.updated_at.isoformat()
        }, status=status.HTTP_200_OK)
    
    def _validate_image(self, image):
        """
        Valida que el archivo sea una imagen válida.
        """
        # Validar que sea una imagen
        if not image.content_type.startswith('image/'):
            return Response({'error': 'El archivo debe ser una imagen'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar tamaño (máximo 5MB)
        if image.size > 5 * 1024 * 1024:
            return Response({'error': 'La imagen no puede ser mayor a 5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        return None


def index(request):
    """
    Vista para renderizar la página principal de terapeutas.
    """
    return render(request, "therapists_ui.html")
