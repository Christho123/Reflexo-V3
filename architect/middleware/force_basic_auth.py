from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.contrib.auth import authenticate
import base64
import re


class ForceBasicAuthMiddleware(MiddlewareMixin):
    """
    Middleware que fuerza la autenticación básica para endpoints específicos
    """
    
    # Rutas que NO requieren autenticación básica
    EXEMPT_PATHS = [
        r'^/api/architect/auth/login/',
        r'^/api/architect/auth/register/',
        r'^/admin/',
        r'^/health/',
        r'^/static/',
        r'^/media/',
    ]
    
    def process_request(self, request):
        # Verificar si la ruta está exenta
        for pattern in self.EXEMPT_PATHS:
            if re.match(pattern, request.path):
                return None
        
        # Verificar si es una ruta de API
        if not request.path.startswith('/api/'):
            return None
            
        # Verificar si ya hay autenticación
        if hasattr(request, 'user') and request.user.is_authenticated:
            return None
            
        # Verificar header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Basic '):
            return self._unauthorized_response()
            
        try:
            # Decodificar credenciales
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Autenticar usuario
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                request.user = user
                return None
            else:
                return self._unauthorized_response()
                
        except (ValueError, IndexError, UnicodeDecodeError):
            return self._unauthorized_response()
    
    def _unauthorized_response(self):
        """Retorna respuesta 401 con header WWW-Authenticate"""
        response = HttpResponse('Autenticación requerida', status=401)
        response['WWW-Authenticate'] = 'Basic realm="API"'
        return response

