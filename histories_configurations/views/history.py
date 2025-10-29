import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from ..models.history import History
from ..models.document_type import DocumentType

@csrf_exempt
def histories_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = History.objects.filter(deleted_at__isnull=True).select_related("patient", "contraceptive_method", "diu_type")
    data = []
    for h in qs:
        data.append({
            "id": h.id,
            "patient": {
                "id": h.patient.id,
                "name": h.patient.name,
                "paternal_lastname": h.patient.paternal_lastname,
                "maternal_lastname": h.patient.maternal_lastname,
                "full_name": h.patient.get_full_name(),
                "document_number": h.patient.document_number,
                "email": h.patient.email,
                "phone1": h.patient.phone1,
                "phone2": h.patient.phone2,
            },
            "history_date": h.history_date.isoformat() if h.history_date else None,
            "testimony": h.testimony,
            "private_observation": h.private_observation,
            "observation": h.observation,
            "height": float(h.height) if h.height else None,
            "initial_weight": h.initial_weight,
            "last_weight": float(h.last_weight) if h.last_weight else None,
            "actual_weight": h.actual_weight,
            "menstruation": h.menstruation,
            "diu_type": (
                {"id": h.diu_type_id, "name": h.diu_type.name}
                if h.diu_type else None
            ),
            "gestation": h.gestation,
            "contraceptive_method": (
                {"id": h.contraceptive_method_id, "name": h.contraceptive_method.name}
                if h.contraceptive_method else None
            ),
            "created_at": h.created_at.isoformat() if h.created_at else None,
            "updated_at": h.updated_at.isoformat() if h.updated_at else None,
            "deleted_at": h.deleted_at.isoformat() if h.deleted_at else None
        })
    return JsonResponse({"histories": data})


@csrf_exempt
def history_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    # Manejo de JSON inválido
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)
    
    patient_id = payload.get("patient")
    history_date = payload.get("history_date")
    contraceptive_method_id = payload.get("contraceptive_method")
    diu_type_id = payload.get("diu_type")

    # Validar campos obligatorios
    if patient_id is None or history_date is None:
        return JsonResponse({"error": "Campos obligatorios faltantes: patient y history_date"}, status=400)

    # Verificar si ya existe un historial activo para este paciente en esta fecha
    existing_history = History.objects.filter(
        patient_id=patient_id,
        history_date=history_date,
        deleted_at__isnull=True
    ).first()
    
    if existing_history:
        return JsonResponse({
            "error": "Ya existe un historial para este paciente en esta fecha",
            "existing_history_id": existing_history.id,
            "history_date": history_date
        }, status=409)
    
    try:
        # Preparar datos para crear el historial
        history_data = {
            'patient_id': patient_id,
            'history_date': history_date,
            'testimony': payload.get('testimony', True),
            'private_observation': payload.get('private_observation'),
            'observation': payload.get('observation'),
            'height': payload.get('height'),
            'initial_weight': payload.get('initial_weight'),
            'last_weight': payload.get('last_weight'),
            'actual_weight': payload.get('actual_weight'),
            'menstruation': payload.get('menstruation', True),
            'diu_type_id': diu_type_id,
            'gestation': payload.get('gestation', True),
            'contraceptive_method_id': contraceptive_method_id,
        }
        
        # Filtrar valores None para campos opcionales
        filtered_data = {k: v for k, v in history_data.items() if v is not None}
        
        h = History.objects.create(**filtered_data)
        
        # Preparar respuesta con todos los campos del historial creado
        response_data = {
            "message": "Historial creado exitosamente",
            "history": {
                "id": h.id,
                "patient": {
                    "id": h.patient.id,
                    "name": h.patient.name,
                    "paternal_lastname": h.patient.paternal_lastname,
                    "maternal_lastname": h.patient.maternal_lastname,
                    "full_name": h.patient.get_full_name(),
                    "document_number": h.patient.document_number,
                    "email": h.patient.email,
                    "phone1": h.patient.phone1,
                    "phone2": h.patient.phone2,
                },
                "history_date": str(h.history_date) if h.history_date else None,
                "testimony": h.testimony,
                "private_observation": h.private_observation,
                "observation": h.observation,
                "height": float(h.height) if h.height else None,
                "initial_weight": h.initial_weight,
                "last_weight": float(h.last_weight) if h.last_weight else None,
                "actual_weight": h.actual_weight,
                "menstruation": h.menstruation,
                "diu_type": (
                    {"id": h.diu_type_id, "name": h.diu_type.name}
                    if h.diu_type else None
                ),
                "gestation": h.gestation,
                "contraceptive_method": (
                    {"id": h.contraceptive_method_id, "name": h.contraceptive_method.name}
                    if h.contraceptive_method else None
                ),
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "updated_at": h.updated_at.isoformat() if h.updated_at else None,
                "deleted_at": h.deleted_at.isoformat() if h.deleted_at else None
            }
        }
        
        return JsonResponse(response_data, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error al crear el historial: {str(e)}"}, status=500)

@csrf_exempt
def history_update(request, pk):
    """
    Endpoint PUT para actualizar un historial médico existente
    """
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"])
    
    try:
        # Buscar el historial activo
        history = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error": "Historial no encontrado o eliminado"}, status=404)
    
    # Manejo de JSON inválido
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return JsonResponse({"error": f"Error al procesar JSON: {str(e)}"}, status=400)
    
    # Campos permitidos para actualización
    allowed_fields = {
        'testimony': 'testimony',
        'private_observation': 'private_observation',
        'observation': 'observation',
        'height': 'height',
        'initial_weight': 'initial_weight',
        'last_weight': 'last_weight',
        'actual_weight': 'actual_weight',
        'menstruation': 'menstruation',
        'diu_type': 'diu_type_id',
        'gestation': 'gestation',
        'patient': 'patient_id',  # Si se permite cambiar el paciente
        'history_date': 'history_date',  # Fecha del historial
        'contraceptive_method': 'contraceptive_method_id',
    }
    
    # Validar que no exista otro historial activo para el mismo paciente y fecha
    new_patient_id = payload.get('patient', history.patient_id)
    new_history_date = payload.get('history_date', history.history_date)
    
    if new_patient_id and new_history_date:
        existing_history = History.objects.filter(
            patient_id=new_patient_id,
            history_date=new_history_date,
            deleted_at__isnull=True
        ).exclude(pk=pk).first()
        
        if existing_history:
            return JsonResponse({
                "error": "Ya existe un historial para este paciente en esta fecha",
                "existing_history_id": existing_history.id,
                "history_date": new_history_date
            }, status=409)
    
    try:
        with transaction.atomic():
            # Actualizar campos permitidos
            for field_name, model_field in allowed_fields.items():
                if field_name in payload:
                    value = payload[field_name]
                    
                    # Convertir valores booleanos si es necesario
                    if field_name in ['testimony', 'menstruation', 'gestation']:
                        if isinstance(value, str):
                            value = value.lower() in ('true', '1', 'yes', 'si')
                    
                    # Para campos decimales, manejar valores vacíos
                    if field_name in ['height', 'last_weight']:
                        if value == '' or value is None:
                            setattr(history, model_field, None)
                        else:
                            setattr(history, model_field, value)
                    else:
                        setattr(history, model_field, value)
            
            # Guardar los cambios
            history.save()
            
            # Preparar respuesta con datos actualizados
            updated_data = {
                "id": history.id,
                "patient": history.patient_id,
                "history_date": str(history.history_date) if history.history_date else None,
                "testimony": history.testimony,
                "private_observation": history.private_observation,
                "observation": history.observation,
                "height": float(history.height) if history.height else None,
                "initial_weight": history.initial_weight,
                "last_weight": float(history.last_weight) if history.last_weight else None,
                "actual_weight": history.actual_weight,
                "menstruation": history.menstruation,
                "diu_type": (
                    {"id": history.diu_type_id, "name": history.diu_type.name}
                    if history.diu_type else None
                ),
                "gestation": history.gestation,
                "contraceptive_method": (
                    {"id": history.contraceptive_method_id, "name": history.contraceptive_method.name}
                    if history.contraceptive_method else None
                ),
                "updated_at": history.updated_at.isoformat() if history.updated_at else None
            }
            
            return JsonResponse({
                "message": "Historial actualizado exitosamente",
                "history": updated_data
            }, status=200)
            
    except Exception as e:
        return JsonResponse({"error": f"Error al actualizar el historial: {str(e)}"}, status=500)

@csrf_exempt
def history_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    
    h.delete()
    return JsonResponse({"status": "deleted"})

@csrf_exempt
def history_detail(request, pk):
    """
    GET - Obtener historial específico
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    try:
        history = History.objects.filter(deleted_at__isnull=True).select_related("patient", "contraceptive_method", "diu_type").get(pk=pk)
        data = {
            "id": history.id,
            "patient": {
                "id": history.patient.id,
                "name": history.patient.name,
                "paternal_lastname": history.patient.paternal_lastname,
                "maternal_lastname": history.patient.maternal_lastname,
                "full_name": history.patient.get_full_name(),
                "document_number": history.patient.document_number,
                "email": history.patient.email,
                "phone1": history.patient.phone1,
                "phone2": history.patient.phone2,
            },
            "history_date": history.history_date.isoformat() if history.history_date else None,
            "testimony": history.testimony,
            "private_observation": history.private_observation,
            "observation": history.observation,
            "height": float(history.height) if history.height else None,
            "initial_weight": history.initial_weight,
            "last_weight": float(history.last_weight) if history.last_weight else None,
            "actual_weight": history.actual_weight,
            "menstruation": history.menstruation,
            "diu_type": (
                {"id": history.diu_type_id, "name": history.diu_type.name}
                if history.diu_type else None
            ),
            "gestation": history.gestation,
            "contraceptive_method": (
                {"id": history.contraceptive_method_id, "name": history.contraceptive_method.name}
                if history.contraceptive_method else None
            ),
            "created_at": history.created_at.isoformat() if history.created_at else None,
            "updated_at": history.updated_at.isoformat() if history.updated_at else None,
            "deleted_at": history.deleted_at.isoformat() if history.deleted_at else None
        }
        return JsonResponse(data)
    except History.DoesNotExist:
        return JsonResponse({"error": "Historial no encontrado"}, status=404)

@csrf_exempt
def patient_history(request, patient_id):
    """
    GET - Obtener historial de paciente específico
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    try:
        history = History.objects.filter(
            patient_id=patient_id, 
            deleted_at__isnull=True
        ).select_related("patient", "contraceptive_method").first()
        
        if not history:
            return JsonResponse({"error": "No se encontró historial para este paciente"}, status=404)
        
        data = {
            "id": history.id,
            "patient": {
                "id": history.patient.id,
                "name": history.patient.name,
                "paternal_lastname": history.patient.paternal_lastname,
                "maternal_lastname": history.patient.maternal_lastname,
                "full_name": history.patient.get_full_name(),
                "document_number": history.patient.document_number,
                "email": history.patient.email,
                "phone1": history.patient.phone1,
                "phone2": history.patient.phone2,
            },
            "history_date": history.history_date.isoformat() if history.history_date else None,
            "testimony": history.testimony,
            "private_observation": history.private_observation,
            "observation": history.observation,
            "height": float(history.height) if history.height else None,
            "initial_weight": history.initial_weight,
            "last_weight": float(history.last_weight) if history.last_weight else None,
            "actual_weight": history.actual_weight,
            "menstruation": history.menstruation,
            "diu_type": (
                {"id": history.diu_type_id, "name": history.diu_type.name}
                if history.diu_type else None
            ),
            "gestation": history.gestation,
            "contraceptive_method": (
                {"id": history.contraceptive_method_id, "name": history.contraceptive_method.name}
                if history.contraceptive_method else None
            ),
            "created_at": history.created_at.isoformat() if history.created_at else None,
            "updated_at": history.updated_at.isoformat() if history.updated_at else None,
            "deleted_at": history.deleted_at.isoformat() if history.deleted_at else None
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": f"Error al obtener el historial: {str(e)}"}, status=500)