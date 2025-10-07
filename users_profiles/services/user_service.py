from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

User = get_user_model()

class UserService:
    """Servicio para lógica de negocio relacionada con usuarios"""
    
    @staticmethod
    def create_user(user_data):
        """Crear un nuevo usuario con perfil básico"""
        try:
            with transaction.atomic():
                # Crear el usuario
                user = User.objects.create_user(
                    user_name=user_data['user_name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    name=user_data.get('name', ''),
                    paternal_lastname=user_data.get('paternal_lastname', ''),
                    maternal_lastname=user_data.get('maternal_lastname', '')
                )
                
                return user
                
        except Exception as e:
            raise ValidationError(f"Error al crear usuario: {str(e)}")
    
    @staticmethod
    def update_user(user, user_data):
        """Actualizar información del usuario"""
        try:
            with transaction.atomic():
                # Actualizar campos del usuario
                for field, value in user_data.items():
                    if hasattr(user, field):
                        setattr(user, field, value)
                
                user.save()
                return user
                
        except Exception as e:
            raise ValidationError(f"Error al actualizar usuario: {str(e)}")
    
    @staticmethod
    def update_profile_photo(user, photo_url):
        """Actualiza la foto de perfil del usuario"""
        try:
            # Asignar nueva foto
            user.photo_url = photo_url
            user.save()
            
            return user
            
        except Exception as e:
            raise ValidationError(f"Error al actualizar foto de perfil: {str(e)}")
    
    @staticmethod
    def delete_profile_photo(user):
        """Eliminar foto de perfil del usuario"""
        try:
            user.photo_url = None
            user.save()
            return True
            
        except Exception as e:
            raise ValidationError(f"Error al eliminar foto de perfil: {str(e)}")
    
    @staticmethod
    def search_users(query, limit=20):
        """Buscar usuarios por nombre o username"""
        try:
            from django.db.models import Q
            
            queryset = User.objects.filter(is_active=True)
            
            if query:
                queryset = queryset.filter(
                    Q(user_name__icontains=query) |
                    Q(name__icontains=query) |
                    Q(paternal_lastname__icontains=query)
                )
            
            return queryset[:limit]
            
        except Exception as e:
            raise ValidationError(f"Error en búsqueda de usuarios: {str(e)}")
    
    @staticmethod
    def get_user_by_username(user_name):
        """Obtiene un usuario por username"""
        try:
            return User.objects.get(user_name=user_name, is_active=True)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """Obtener usuario por email"""
        try:
            return User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def deactivate_user(user):
        """Desactivar usuario"""
        try:
            user.is_active = False
            user.save()
            return True
        except Exception as e:
            raise ValidationError(f"Error al desactivar usuario: {str(e)}")
    
    @staticmethod
    def activate_user(user):
        """Activar usuario"""
        try:
            user.is_active = True
            user.save()
            return True
        except Exception as e:
            raise ValidationError(f"Error al activar usuario: {str(e)}")
    
    @staticmethod
    def get_user_stats(user):
        """Obtener estadísticas del usuario"""
        try:
            stats = {
                'user_name': user.user_name,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'has_profile_photo': bool(user.photo_url),
                'profile_completion': 0
            }
            
            # Calcular completitud del perfil
            required_fields = ['name', 'email', 'phone']
            completed_fields = sum(1 for field in required_fields if getattr(user, field))
            stats['profile_completion'] = (completed_fields / len(required_fields)) * 100
            
            return stats
            
        except Exception as e:
            raise ValidationError(f"Error al obtener estadísticas: {str(e)}")