import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.diagnosis import Diagnosis

class DiagnosisListView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación
    
    def get(self, request):
        try:
            qs = Diagnosis.objects.all()
            data = [{"id": x.id, "code": x.code, "name": x.name} for x in qs]
            return Response({"diagnoses": data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Mantener la función original para compatibilidad (pero ahora con autenticación)
@csrf_exempt
def diagnosis_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        qs = Diagnosis.objects.all()
        data = [{"id": x.id, "code": x.code, "name": x.name} for x in qs]
        return JsonResponse({"diagnoses": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class DiagnosisCreateView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación
    
    def post(self, request):
        code = request.data.get("code", "")
        name = request.data.get("name", "")
        
        d = Diagnosis.objects.create(code=code, name=name)
        return Response({
            "id": d.id,
            "code": d.code,
            "name": d.name
        }, status=status.HTTP_201_CREATED)

# Mantener la función original para compatibilidad
@csrf_exempt
def diagnosis_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payload = json.loads(request.body.decode() or "{}")
    
    code = payload.get("code", "")
    name = payload.get("name", "")

    d = Diagnosis.objects.create(code=code, name=name)

    return JsonResponse({
        "id": d.id,
        "code": d.code,
        "name": d.name
    }, status=201)

class DiagnosisDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación
    
    def delete(self, request, pk):
        try:
            d = Diagnosis.objects.get(pk=pk)
        except Diagnosis.DoesNotExist:
            return Response({"error": "Diagnostico no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            d.delete()
            return Response({"status": "deleted", "id": pk}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al eliminar el Diagnostico: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Mantener la función original para compatibilidad
@csrf_exempt
def diagnosis_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        d = Diagnosis.objects.get(pk=pk)
    except Diagnosis.DoesNotExist:
        return JsonResponse({"error": "Diagnostico no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    
    try:
        d.delete()
        return JsonResponse({"status": "deleted", "id": pk}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al eliminar el Diagnostico: {str(e)}"}, status=500)


class DiagnosisEditView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requiere autenticación
    
    def put(self, request, pk):
        try:
            d = Diagnosis.objects.get(pk=pk)
        except Diagnosis.DoesNotExist:
            return Response({"error": "Diagnostico no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error al buscar el Diagnostico: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            if "code" in request.data:
                d.code = request.data["code"]
            if "name" in request.data:
                d.name = request.data["name"]

            d.save()

            return Response({
                "id": d.id,
                "code": d.code,
                "name": d.name
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error inesperado al editar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Mantener la función original para compatibilidad
@csrf_exempt
def diagnosis_edit(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    try:
        d = Diagnosis.objects.get(pk=pk)
    except Diagnosis.DoesNotExist:
        return JsonResponse({"error": "Diagnostico no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error al buscar el Diagnostico: {str(e)}"}, status=500)

    try:
        payload = json.loads(request.body.decode() or "{}")

        if "code" in payload:
            d.code = payload["code"]
        if "name" in payload:
            d.name = payload["name"]

        d.save()

        return JsonResponse({
            "id": d.id,
            "code": d.code,
            "name": d.name
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud no es un JSON válido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado al editar: {str(e)}"}, status=500)
