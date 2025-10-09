import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers.diu_type import DIUTypeSerializer
from ..services import diu_type_service as service


def _json_body(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}


@csrf_exempt
@api_view(["GET"]) 
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def diu_type_list(request):
    items = service.list_active()
    data = DIUTypeSerializer(items, many=True).data
    return JsonResponse({"diu_type": data})


@csrf_exempt
@api_view(["POST"]) 
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def diu_type_create(request):
    payload = _json_body(request)
    serializer = DIUTypeSerializer(data=payload)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    obj = service.create(**serializer.validated_data)
    return JsonResponse(DIUTypeSerializer(obj).data, status=201)


@csrf_exempt
@api_view(["PUT", "PATCH"]) 
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def diu_type_edit(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)

    payload = _json_body(request)
    serializer = DIUTypeSerializer(obj, data=payload, partial=True)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    obj = service.update(obj, **serializer.validated_data)
    return JsonResponse(DIUTypeSerializer(obj).data, status=200)


@csrf_exempt
@api_view(["DELETE"]) 
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def diu_type_delete(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)
    service.soft_delete(obj)
    return JsonResponse({"status": "deleted", "id": pk}, status=200)


@csrf_exempt
@api_view(["GET"]) 
@authentication_classes([JWTAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def diu_type_detail(request, pk: int):
    obj = service.get_by_id(pk)
    if obj is None:
        return JsonResponse({"error": "No encontrado"}, status=404)
    return JsonResponse(DIUTypeSerializer(obj).data, status=200)