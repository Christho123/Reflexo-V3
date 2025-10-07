# users_profiles/views/profile.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import get_user_model

# Serializers
from ..serializers.profile import (
    ProfileSerializer, ProfileUpdateSerializer, ProfileCreateSerializer,
    PublicProfileSerializer, ProfileSettingsSerializer
)

User = get_user_model()

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Vista para obtener y actualizar el perfil del usuario autenticado.
    Ahora trabajamos directamente con el CustomUser (AUTH_USER_MODEL).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Retorna el serializer apropiado según el método HTTP"""
        if self.request.method == 'GET':
            return ProfileSerializer
        return ProfileUpdateSerializer

    def get_object(self):
        """Obtiene el usuario autenticado"""
        return self.request.user
    def update(self, request, *args, **kwargs):
        """Actualiza los datos del usuario"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Perfil actualizado exitosamente',
            'profile': ProfileSerializer(instance, context={'request': request}).data,
        })


class ProfileCreateView(generics.CreateAPIView):
    """
    Vista para crear un 'perfil'.
    Si realmente usas solo el CustomUser, esta vista probablemente no sea necesaria.
    La dejo para compatibilidad, asumiendo que tu serializer crea/actualiza sobre el propio usuario.
    """

    serializer_class = ProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Crea el perfil asociado al usuario autenticado"""
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Asumimos que el serializer trabaja sobre request.user o devuelve datos del usuario
        return Response({
            'message': 'Perfil creado/actualizado exitosamente',
            'profile': ProfileSerializer(request.user, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED)


class PublicProfileView(generics.RetrieveAPIView):
    """
    Vista para obtener perfiles 'públicos'. Dado que tu modelo no tiene is_public,
    usamos is_active=True como criterio básico (ajústalo si tu lógica de “público” es otra).
    """

    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_active=True)
    
    def get_object(self):
        """Retorna el usuario por username"""
        user_name = self.kwargs.get('user_name')
        return get_object_or_404(
            User,
            user_name=user_name,
            is_active=True
        )


class ProfileSettingsView(generics.UpdateAPIView):
    """
    Vista para actualizar configuraciones del 'perfil' del usuario.
    Operamos directamente sobre request.user.
    """

    serializer_class = ProfileSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Obtiene el usuario autenticado"""
        return self.request.user
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Configuraciones del perfil actualizadas exitosamente',
            'settings': ProfileSettingsSerializer(instance).data,
        })


class ProfileCompletionView(APIView):
    """
    Vista para obtener el porcentaje de completitud del perfil.
    Trabajamos con el CustomUser directamente.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retorna el porcentaje de completitud del perfil"""
        user = request.user
        
        # Calcular completitud del perfil
        required_fields = ['name', 'email', 'phone']
        completed_fields = sum(1 for field in required_fields if getattr(user, field))
        completion_percentage = (completed_fields / len(required_fields)) * 100
        
        return Response({
            'completion_percentage': completion_percentage,
            'is_complete': completion_percentage >= 80,
            'missing_fields': self._get_missing_fields(user)
        })
    
    def _get_missing_fields(self, user):
        """Retorna los campos que faltan para completar el perfil"""
        missing = []
        
        if not user.name:
            missing.append('name')
        if not user.email:
            missing.append('email')
        if not user.phone:
            missing.append('phone')
        if not user.photo_url:
            missing.append('photo_url')
        
        return missing


class ProfileSearchView(generics.ListAPIView):
    """
    Vista para buscar 'perfiles' públicos.
    Sin 'is_public', usamos is_active=True como filtro base.
    """

    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_active=True)
    
    def get_queryset(self):
        """Filtra usuarios según parámetros de búsqueda"""
        queryset = super().get_queryset()
        # Búsqueda por nombre
        name_query = self.request.query_params.get('name')
        if name_query:
            queryset = queryset.filter(
                models.Q(name__icontains=name_query) |
                models.Q(paternal_lastname__icontains=name_query) |
                models.Q(maternal_lastname__icontains=name_query) |
                models.Q(username__icontains=name_query) |
                models.Q(email__icontains=name_query)
            )
        
        # Filtro por género
        sex = self.request.query_params.get('sex', None)
        if sex:
            queryset = queryset.filter(sex=sex)
        
        # Filtro por país
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__name__icontains=country)
        
        return queryset[:50]  # Limitar a 50 resultados
