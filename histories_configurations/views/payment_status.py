import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models.payment_status import PaymentStatus


@csrf_exempt
def payment_status_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        qs = PaymentStatus.objects.all()
        data = [{"id": x.id, "name": x.name, "description": x.description} for x in qs]
        return JsonResponse({"payment_status": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def payment_status_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payload = json.loads(request.body.decode() or "{}")

    name = payload.get("name", "")
    description = payload.get("description", "")

    dt = PaymentStatus.objects.create(name=name, description=description)

    return JsonResponse({
        "id": dt.id,
        "name": dt.name,
        "description": dt.description
    }, status=201)

@csrf_exempt
def payment_status_edit(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    try:
        dt = PaymentStatus.objects.get(pk=pk)
    except PaymentStatus.DoesNotExist:
        return JsonResponse({"error": "Estado de Pago no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error al buscar el estado de Pago: {str(e)}"}, status=500)

    try:
        payload = json.loads(request.body.decode() or "{}")

        if "name" in payload:
            dt.name = payload["name"]
        if "description" in payload:
            dt.description = payload["description"]

        dt.save()

        return JsonResponse({
            "id": dt.id,
            "name": dt.name,
            "description": dt.description
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud no es un JSON válido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado al editar: {str(e)}"}, status=500)

@csrf_exempt
def payment_status_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        # Intentamos obtener el tipo de documento por su pk
        dt = PaymentStatus.objects.get(pk=pk)
    except PaymentStatus.DoesNotExist:
        return JsonResponse({"error": "Estado de Pago no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    
    try:
        dt.delete()
        return JsonResponse({"status": "deleted", "id": pk}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al eliminar el documento: {str(e)}"}, status=500)