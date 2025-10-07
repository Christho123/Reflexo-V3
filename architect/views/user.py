from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ..serializers.user import UserSerializer

User = get_user_model()

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    # GET - Listar todos los usuarios o buscar usuario específico
    def get(self, request, pk=None):
        if pk is not None:
            # Buscar usuario específico
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {"error": "Usuario no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Listar todos los usuarios
            users = User.objects.all()
            serializer = UserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    # POST - Crear nuevo usuario
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT - Actualizar usuario específico (actualización completa)
    def put(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "Se requiere el ID del usuario"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH - Actualización parcial de usuario
    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "Se requiere el ID del usuario"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Eliminar usuario
    def delete(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "Se requiere el ID del usuario"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Eliminar tokens relacionados antes de eliminar el usuario
            self._cleanup_user_tokens(user)
            
            # Eliminación física permanente - sin rastro
            user.delete()
            message = "Usuario eliminado permanentemente"
            
            return Response(
                {"message": message}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            error_message = str(e)
            
            # Manejar error específico de tabla de verificación inexistente
            if "users_verification_code" in error_message and "doesn't exist" in error_message:
                # Intentar eliminar manualmente sin las relaciones problemáticas
                try:
                    # Eliminar el usuario directamente desde la base de datos
                    from django.db import connection
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM users WHERE id = %s", [pk])
                    
                    return Response(
                        {"message": "Usuario eliminado permanentemente (sin verificación)"}, 
                        status=status.HTTP_200_OK
                    )
                except Exception as e2:
                    return Response(
                        {"error": f"Error al eliminar el usuario: {str(e2)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    {"error": f"Error al eliminar el usuario: {error_message}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    def _cleanup_user_tokens(self, user):
        """
        Elimina todos los tokens relacionados con el usuario para evitar
        errores de restricción de clave foránea
        """
        try:
            # Importar los modelos de token blacklist
            from rest_framework_simplejwt.token_blacklist.models import (
                OutstandingToken, 
                BlacklistedToken
            )
            
            # Eliminar tokens outstanding (activos) del usuario
            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            for token in outstanding_tokens:
                # Eliminar tokens blacklisted relacionados
                BlacklistedToken.objects.filter(token=token).delete()
            
            # Eliminar tokens outstanding
            outstanding_tokens.delete()
            
        except Exception as e:
            # Si hay algún error, intentar limpieza manual con SQL
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    # Eliminar tokens blacklisted primero
                    cursor.execute(
                        "DELETE FROM token_blacklist_blacklistedtoken WHERE token_id IN "
                        "(SELECT id FROM token_blacklist_outstandingtoken WHERE user_id = %s)",
                        [user.id]
                    )
                    # Eliminar tokens outstanding
                    cursor.execute(
                        "DELETE FROM token_blacklist_outstandingtoken WHERE user_id = %s",
                        [user.id]
                    )
            except Exception as sql_error:
                # Log del error pero continuar con la eliminación del usuario
                print(f"Error limpiando tokens para usuario {user.id}: {sql_error}")



class UserPhotoUploadView(APIView):
    """
    Vista para subir fotos de perfil de usuarios.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk=None):
        """
        Sube una foto de perfil para el usuario.
        """
        try:
            if pk is None:
                return Response({
                    "error": "Se requiere el ID del usuario"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(pk=pk)
            
            if 'photo_url' not in request.FILES:
                return Response({'error': 'No se proporcionó archivo de imagen'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que sea una imagen
            image = request.FILES['photo_url']
            if not image.content_type.startswith('image/'):
                return Response({'error': 'El archivo debe ser una imagen'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar tamaño (máximo 5MB)
            if image.size > 5 * 1024 * 1024:
                return Response({'error': 'La imagen no puede ser mayor a 5MB'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Guardar la imagen
            user.photo_url = image
            user.save(update_fields=['photo_url'])
            
            return Response({
                'message': 'Foto de perfil subida exitosamente',
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'photo_url': user.photo_url.url if user.photo_url else None,
                'uploaded_at': user.updated_at.isoformat()
            }, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al subir la foto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        """
        Actualiza/reemplaza la foto de perfil del usuario.
        """
        try:
            if pk is None:
                return Response({
                    "error": "Se requiere el ID del usuario"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(pk=pk)
            
            if 'photo_url' not in request.FILES:
                return Response({'error': 'No se proporcionó archivo de imagen'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que sea una imagen
            image = request.FILES['photo_url']
            if not image.content_type.startswith('image/'):
                return Response({'error': 'El archivo debe ser una imagen'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar tamaño (máximo 5MB)
            if image.size > 5 * 1024 * 1024:
                return Response({'error': 'La imagen no puede ser mayor a 5MB'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Eliminar foto anterior si existe
            if user.photo_url:
                try:
                    user.photo_url.delete(save=False)
                except:
                    pass  # Si no se puede eliminar, continuar
            
            # Guardar la nueva imagen
            user.photo_url = image
            user.save(update_fields=['photo_url'])
            
            return Response({
                'message': 'Foto de perfil actualizada exitosamente',
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'photo_url': user.photo_url.url if user.photo_url else None,
                'updated_at': user.updated_at.isoformat()
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al actualizar la foto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk=None):
        """
        Actualización parcial de la foto de perfil del usuario.
        """
        return self.put(request, pk)  # Mismo comportamiento que PUT

    def delete(self, request, pk=None):
        """
        Elimina la foto de perfil del usuario.
        """
        try:
            if pk is None:
                return Response({
                    "error": "Se requiere el ID del usuario"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(pk=pk)
            
            if not user.photo_url:
                return Response({'error': 'El usuario no tiene foto de perfil'}, status=status.HTTP_404_NOT_FOUND)
            
            # Eliminar la foto
            user.photo_url.delete(save=False)
            user.photo_url = None
            user.save(update_fields=['photo_url'])
            
            return Response({
                'message': 'Foto de perfil eliminada exitosamente',
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'photo_url': None,
                'deleted_at': user.updated_at.isoformat()
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar la foto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)