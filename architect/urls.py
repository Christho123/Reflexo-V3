from django.urls import path
from .views.auth import LoginView, RegisterView, LogoutView
from .views.user import UserView, UserPhotoUploadView
from .views.permission import PermissionView, RoleView

app_name = 'architect'

urlpatterns = [
    # Autenticación
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # Usuarios - Actualizado para soportar todas las operaciones
    path('users/', UserView.as_view(), name='users'),  # GET (listar), POST (crear)
    path('users/<int:pk>/', UserView.as_view(), name='users_detail'),  # GET, PUT, PATCH, DELETE (operaciones específicas)
    path('users/<int:pk>/upload/', UserPhotoUploadView.as_view(), name='user_photo_upload'),  # POST (subir foto)
    
    # Permisos
    path('permissions/', PermissionView.as_view(), name='permissions'),
    
    # Roles
    path('roles/', RoleView.as_view(), name='roles_list'),
    path('roles/<int:pk>/', RoleView.as_view(), name='roles_detail'),
    path('roles/create/', RoleView.as_view(), name='roles_create'),
    path('roles/<int:pk>/edit/', RoleView.as_view(), name='roles_update'),
    path('roles/<int:pk>/delete/', RoleView.as_view(), name='roles_delete'),
]