from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models

# Serializadores locales
from ..serializers.user import (
    UserSerializer, UserUpdateSerializer, UserProfilePhotoSerializer
)

User = get_user_model()
class UserDetailView(generics.RetrieveAPIView):
    """Vista para obtener detalles del usuario autenticado"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retorna el usuario autenticado"""
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    """Vista para actualizar información del usuario"""
    
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retorna el usuario autenticado"""
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Actualiza la información del usuario"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Información del usuario actualizada exitosamente',
            'user': UserSerializer(instance, context={'request': request}).data
        })

class UserProfilePhotoView(APIView):
    """Vista para gestionar la foto de perfil del usuario"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def _handle_photo_upload(self, request, message="Foto de perfil actualizada exitosamente"):
        """Método común para manejar la subida de foto"""
        print(f"DEBUG: request.data = {request.data}")
        print(f"DEBUG: request.FILES = {request.FILES}")
        
        serializer = UserProfilePhotoSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print(f"DEBUG: Errores del serializer: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        updated_user = serializer.save()
        
        # Obtener la URL completa de la foto
        photo_url = None
        if hasattr(updated_user, '_photo_url_full'):
            photo_url = updated_user._photo_url_full
        elif updated_user.photo_url:
            try:
                photo_url = request.build_absolute_uri(updated_user.photo_url.url)
            except Exception as e:
                print(f"DEBUG: Error construyendo URL: {e}")
        
        return Response({
            'message': message,
            'photo_url': photo_url
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Sube una nueva foto de perfil"""
        return self._handle_photo_upload(request, "Foto de perfil subida exitosamente")
    
    def put(self, request):
        """Actualiza la foto de perfil existente"""
        return self._handle_photo_upload(request, "Foto de perfil actualizada exitosamente")
    
    def delete(self, request):
        """Elimina la foto de perfil del usuario"""
        if request.user.photo_url:
            # Eliminar archivo físico si existe
            try:
                import os
                if os.path.isfile(request.user.photo_url.path):
                    os.remove(request.user.photo_url.path)
            except (ValueError, AttributeError):
                pass  # El archivo no existe en el sistema de archivos
            
            request.user.photo_url = None
            request.user.save()
            return Response({
                'message': 'Foto de perfil eliminada exitosamente'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'No tienes una foto de perfil para eliminar'
        }, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    """Vista para buscar usuarios por nombre o username"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra usuarios según el parámetro de búsqueda"""
        queryset = User.objects.filter(is_active=True)
        search_query = self.request.query_params.get('q', None)
        
        if search_query:
            queryset = queryset.filter(
                models.Q(user_name__icontains=search_query) |
                models.Q(name__icontains=search_query) |
                models.Q(paternal_lastname__icontains=search_query)
            )
        
        return queryset[:20]  # Limitar a 20 resultados

class UserProfileView(generics.RetrieveAPIView):
    """Vista para obtener perfil completo del usuario autenticado"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retorna el usuario autenticado"""
        return self.request.user
    
    def get_serializer_context(self):
        """Agrega contexto adicional al serializer"""
        context = super().get_serializer_context()
        context['public_view'] = False  # Es vista privada del usuario autenticado
        return context