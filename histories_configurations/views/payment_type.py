import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models.payment_type import PaymentType

@csrf_exempt
def payment_types_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    qs = PaymentType.objects.filter(deleted_at__isnull=True)
    data = [{"id": x.id, "name": x.name, "description": x.description} for x in qs]
    return JsonResponse({"payment_types": data})

@csrf_exempt
def payment_type_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payload = json.loads(request.body.decode() or "{}")

    pt = PaymentType.objects.create(
        name=payload.get("name", ""),
        description=payload.get("description", "")
    )

    return JsonResponse({"id": pt.id, "name": pt.name, "description": pt.description}, status=201)

@csrf_exempt
def payment_type_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        # Intentamos obtener el tipo de pago por su pk
        pt = PaymentType.objects.get(pk=pk)
    except PaymentType.DoesNotExist:
        return JsonResponse({"error": "Tipo de pago no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    
    try:
        # Si el tipo de pago existe, lo eliminamos
        pt.delete()
        return JsonResponse({"status": "deleted", "id": pk}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al eliminar el tipo de pago: {str(e)}"}, status=500)


@csrf_exempt
def payment_type_edit(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    try:
        pt = PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
    except PaymentType.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)

    payload = json.loads(request.body.decode() or "{}")

    pt.name = payload.get("name", pt.name)
    pt.description = payload.get("description", pt.description)

    pt.save()
    return JsonResponse({
        "id": pt.id,
        "name": pt.name,
        "description": pt.description
    }, status=200)