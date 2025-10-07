from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.patient import Patient
from ..serializers.patient import PatientSerializer, PatientListSerializer
from ..services.patient_service import PatientService

patient_service = PatientService()

class PatientListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def get(self, request):
        if "per_page" in request.GET or "page" in request.GET:
            page_obj = patient_service.get_paginated(request)
            serializer = PatientSerializer(page_obj.object_list, many=True)
            return Response({
                "count": page_obj.paginator.count,
                "num_pages": page_obj.paginator.num_pages,
                "current_page": page_obj.number,
                "results": serializer.data,
            })
        patients = Patient.objects.filter(deleted_at__isnull=True)
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient, created, restored = patient_service.store_or_restore(serializer.validated_data)
            out = PatientSerializer(patient).data
            if created:
                return Response(out, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "El paciente ya existe", "data": out},
                status=status.HTTP_409_CONFLICT
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PatientRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient, data=request.data, partial=True)  # Edición parcial
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = patient_service.update(patient, serializer.validated_data)
            return Response(PatientSerializer(updated).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Edición parcial de paciente - permite editar solo los campos enviados"""
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = patient_service.update(patient, serializer.validated_data)
            return Response(PatientSerializer(updated).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return Response({'error': 'Paciente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Guardar información del paciente antes de eliminarlo
        patient_id = patient.id
        patient_name = patient.get_full_name()
        
        patient_service.destroy(patient)
        
        return Response({
            'message': 'Paciente eliminado exitosamente',
            'id': patient_id,
            'name': patient_name,
            'deleted_at': patient.deleted_at.isoformat() if patient.deleted_at else None
        }, status=status.HTTP_200_OK)


class PatientSearchView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación

    def get(self, request):
        page_obj = patient_service.search_patients(request.GET)
        serializer = PatientSerializer(page_obj.object_list, many=True)
        return Response({
            "count": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number,
            "results": serializer.data,
        })
