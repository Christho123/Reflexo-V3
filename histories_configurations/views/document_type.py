import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models.document_type import DocumentType

@csrf_exempt
def document_types_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        qs = DocumentType.objects.all()
        data = [{"id": x.id, "name": x.name, "description": x.description} for x in qs]
        return JsonResponse({"document_types": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def document_type_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payload = json.loads(request.body.decode() or "{}")

    name = payload.get("name", "")
    description = payload.get("description", "")

    dt = DocumentType.objects.create(name=name, description=description)

    return JsonResponse({
        "id": dt.id,
        "name": dt.name,
        "description": dt.description
    }, status=201)

@csrf_exempt
def document_type_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        # Intentamos obtener el tipo de documento por su pk
        dt = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "Tipo de documento no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    
    try:
        # Si el documento existe, lo eliminamos
        dt.delete()
        return JsonResponse({"status": "deleted", "id": pk}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al eliminar el documento: {str(e)}"}, status=500)


@csrf_exempt
def document_type_edit(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    try:
        dt = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "Tipo de documento no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error al buscar el documento: {str(e)}"}, status=500)

    try:
        # Cargar el payload de la solicitud
        payload = json.loads(request.body.decode() or "{}")

        # Actualizar solo los campos que estén presentes en el payload
        if "name" in payload:
            dt.name = payload["name"]
        if "description" in payload:
            dt.description = payload["description"]

        # Guardar los cambios
        dt.save()

        # Responder con los datos actualizados
        return JsonResponse({
            "id": dt.id,
            "name": dt.name,
            "description": dt.description
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud no es un JSON válido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado al editar: {str(e)}"}, status=500)
