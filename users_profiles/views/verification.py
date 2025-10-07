# users_profiles/views/verification.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Django Core
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404  # por si lo necesitas luego

# Modelos locales
from ..models.user_verification_code import UserVerificationCode

# Serializadores locales
from ..serializers.verification import (
    VerificationCodeSerializer, EmailChangeSerializer,
    EmailChangeConfirmSerializer, VerificationCodeRequestSerializer,
    VerificationCodeResendSerializer, VerificationStatusSerializer
)

# Servicios locales
from ..services.verification_service import VerificationService

User = get_user_model()


class VerificationCodeView(APIView):
    """Vista para solicitar códigos de verificación"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Solicita un código de verificación"""
        serializer = VerificationCodeRequestSerializer(data=request.data)

        if serializer.is_valid():
            verification_type = serializer.validated_data['verification_type']
            target_email = serializer.validated_data.get('target_email')

            try:
                # Usar el servicio de verificación para enviar el email
                VerificationService.send_verification_email(
                    user=request.user,
                    verification_type=verification_type
                )

                return Response({
                    'message': 'Código de verificación enviado exitosamente',
                    'expires_at': timezone.now() + timezone.timedelta(minutes=15),
                    'verification_type': verification_type
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': f'Error al enviar el código de verificación: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationCodeResendView(APIView):
    """Vista para reenviar códigos de verificación"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Reenvía un código de verificación"""
        serializer = VerificationCodeResendSerializer(data=request.data)

        if serializer.is_valid():
            verification_type = serializer.validated_data['verification_type']
            target_email = serializer.validated_data.get('target_email')

            try:
                # Usar el servicio de verificación para reenviar el email
                VerificationService.resend_verification_email(
                    user=request.user,
                    verification_type=verification_type
                )

                return Response({
                    'message': 'Nuevo código de verificación enviado exitosamente',
                    'expires_at': timezone.now() + timezone.timedelta(minutes=15)
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': f'Error al reenviar el código de verificación: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationStatusView(APIView):
    """Vista para obtener el estado de verificación del usuario"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retorna el estado de verificación del usuario"""
        user = request.user

        # Obtener códigos de verificación activos
        active_codes = UserVerificationCode.objects.filter(
            user=user,
            is_used=False
        ).order_by('-created_at')

        verification_status = []
        for code in active_codes:
            status_data = {
                'verification_type': code.verification_type,
                'expires_at': code.expires_at,
                'attempts_remaining': code.max_attempts - code.attempts,
                'is_valid': code.is_valid()
            }
            verification_status.append(status_data)

        return Response({
            'user_email': user.email,
            # ✅ tu modelo expone email_verified_at, no email_verified
            'email_verified': bool(getattr(user, 'email_verified_at', None)),
            'active_verifications': verification_status
        })


class EmailChangeView(APIView):
    """Vista para solicitar cambio de email"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Solicita cambio de email"""
        serializer = EmailChangeSerializer(data=request.data)

        if serializer.is_valid():
            new_email = serializer.validated_data['new_email']

            try:
                # Usar el servicio de verificación para solicitar cambio de email
                VerificationService.request_email_change(
                    user=request.user,
                    new_email=new_email
                )

                return Response({
                    'message': 'Se ha enviado un código de verificación a tu nuevo email',
                    'expires_at': timezone.now() + timezone.timedelta(minutes=15),
                    'target_email': new_email
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': f'Error al solicitar cambio de email: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailChangeConfirmView(APIView):
    """Vista para confirmar cambio de email"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Confirma el cambio de email"""
        serializer = EmailChangeConfirmSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']

            # Buscar el código de verificación
            try:
                verification = UserVerificationCode.objects.get(
                    user=request.user,
                    code=code,
                    verification_type='email_change',
                    is_used=False
                )

                if verification.is_expired():
                    return Response({'error': 'El código de verificación ha expirado'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if not verification.can_attempt():
                    return Response({'error': 'Demasiados intentos fallidos'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Cambiar el email y marcar verificado ahora (si es tu regla)
                new_email = verification.target_email
                
                # Verificar que el email objetivo existe
                if not new_email:
                    return Response({
                        'error': 'El código de verificación no tiene un email objetivo válido'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                request.user.email = new_email
                # ✅ usamos timestamp en lugar de booleano
                setattr(request.user, 'email_verified_at', timezone.now())
                request.user.save()

                # Marcar el código como usado
                verification.mark_as_used()

                return Response({
                    'message': 'Email cambiado exitosamente',
                    'new_email': new_email
                }, status=status.HTTP_200_OK)

            except UserVerificationCode.DoesNotExist:
                return Response({'error': 'Código de verificación inválido'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """Vista para solicitar verificación de email de registro"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Solicita verificación de email"""
        serializer = VerificationCodeRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('target_email')

            if not email:
                return Response({'error': 'El email es requerido'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)

                # ✅ usa email_verified_at
                if getattr(user, 'email_verified_at', None):
                    return Response({'error': 'Este email ya está verificado'},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                # Usar el servicio de verificación para enviar el email
                VerificationService.send_verification_email(
                    user=user,
                    verification_type='email_verification'
                )

                return Response({
                    'message': 'Código de verificación enviado exitosamente',
                    'expires_at': timezone.now() + timezone.timedelta(minutes=15)
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'No existe una cuenta con este email'},
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': f'Error al enviar el código de verificación: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationConfirmView(APIView):
    """Vista para confirmar verificación de email de registro"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Confirma la verificación de email"""
        serializer = EmailChangeConfirmSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']

            # Buscar el código de verificación
            try:
                verification = UserVerificationCode.objects.get(
                    code=code,
                    verification_type='email_verification',
                    is_used=False
                )

                if verification.is_expired():
                    return Response({'error': 'El código de verificación ha expirado'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if not verification.can_attempt():
                    return Response({'error': 'Demasiados intentos fallidos'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Marcar email como verificado (timestamp)
                user = verification.user
                setattr(user, 'email_verified_at', timezone.now())
                user.save()
                # Marcar el código como usado
                verification.mark_as_used()

                return Response({'message': 'Email verificado exitosamente'},
                                status=status.HTTP_200_OK)

            except UserVerificationCode.DoesNotExist:
                return Response({'error': 'Código de verificación inválido'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
