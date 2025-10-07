from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileService:
    """
    Servicio para gestion de perfiles de usuario.
    """
    
    @staticmethod
    def create_profile(user, profile_data):
        """
        Crear un perfil para un usuario
        
        Args:
            user: Usuario al que se le creara el perfil
            profile_data: Datos del perfil
            
        Returns:
            User: Usuario actualizado
        """
        try:
            with transaction.atomic():
                # Actualizar campos del usuario
                for field, value in profile_data.items():
                    if hasattr(user, field):
                        setattr(user, field, value)
                
                user.save()
                return user
                
        except Exception as e:
            raise ValidationError(f"Error al crear el perfil: {str(e)}")
    
    @staticmethod
    def update_profile(user, profile_data):
        """
        Actualizar el perfil de un usuario
        
        Args:
            user: Usuario cuyo perfil se actualizara
            profile_data: Datos a actualizar
            
        Returns:
            User: Usuario actualizado
        """
        try:
            with transaction.atomic():
                # Actualizar campos
                for field, value in profile_data.items():
                    if hasattr(user, field):
                        setattr(user, field, value)
                
                user.save()
                return user
                
        except Exception as e:
            raise ValidationError(f"Error al actualizar el perfil: {str(e)}")
    
    @staticmethod
    def get_profile_by_user(user):
        """
        Obtener el perfil de un usuario
        
        Args:
            user: Usuario del cual obtener el perfil
            
        Returns:
            User: Usuario con su perfil
        """
        return user
    
    @staticmethod
    def get_public_profiles():
        """
        Obtener todos los perfiles publicos
        
        Returns:
            QuerySet: Usuarios activos
        """
        return User.objects.filter(is_active=True)
    
    @staticmethod
    def get_profile_by_username(user_name):
        """
        Obtener perfil por username
        
        Args:
            user_name: Username del usuario
            
        Returns:
            User: Usuario o None si no existe
        """
        try:
            return User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def calculate_profile_completion(user):
        """
        Calcular el porcentaje de completitud del perfil
        
        Args:
            user: Usuario a evaluar
            
        Returns:
            int: Porcentaje de completitud (0-100)
        """
        # Campos obligatorios que deben estar completos
        required_fields = [
            'name', 'email', 'phone'
        ]
        
        # Campos opcionales que mejoran el perfil
        optional_fields = [
            'paternal_lastname', 'maternal_lastname', 'photo_url', 'document_number'
        ]
        
        total_fields = len(required_fields) + len(optional_fields)
        completed_fields = 0
        
        # Verificar campos requeridos (peso completo)
        for field in required_fields:
            if getattr(user, field):
                completed_fields += 1
        
        # Verificar campos opcionales (peso reducido)
        for field in optional_fields:
            if getattr(user, field):
                completed_fields += 0.5
        
        # Calcular porcentaje y limitar a 100
        return min(100, int((completed_fields / total_fields) * 100))
    
    @staticmethod
    def get_profile_stats(user):
        """
        Obtener estadisticas del perfil
        
        Args:
            user: Usuario a analizar
            
        Returns:
            dict: Estadisticas del perfil
        """
        return {
            'completion_percentage': ProfileService.calculate_profile_completion(user),
            'is_complete': ProfileService.calculate_profile_completion(user) >= 80,
            'account_statement': user.account_statement,
            'is_active': user.is_active
        }
    
    @staticmethod
    def toggle_profile_visibility(user):
        """
        Cambiar la visibilidad del perfil
        
        Args:
            user: Usuario a modificar
            
        Returns:
            User: Usuario actualizado
        """
        user.account_statement = 'I' if user.account_statement == 'A' else 'A'
        user.save()
        return user
    
    @staticmethod
    def update_privacy_settings(user, privacy_data):
        """
        Actualizar configuraciones de privacidad
        
        Args:
            user: Usuario a modificar
            privacy_data: Datos de privacidad
            
        Returns:
            User: Usuario actualizado
        """
        if 'account_statement' in privacy_data:
            user.account_statement = privacy_data['account_statement']
        
        user.save()
        return user
