from typing import Any, Dict, Tuple

from rest_framework.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Concat

from ..models.patient import Patient
from ..serializers.patient import PatientSerializer, PatientListSerializer
from ubi_geo.models import Region, Province, District


class PatientService:
    def get_all(self):
        return Patient.objects.filter(deleted_at__isnull=True)

    def get_paginated(self, request):
        per_page_raw = request.GET.get("per_page", 20)
        page_raw = request.GET.get("page", 1)
        try:
            per_page = int(per_page_raw)
        except (TypeError, ValueError):
            per_page = 20
        try:
            page = int(page_raw)
        except (TypeError, ValueError):
            page = 1
            
        queryset = Patient.objects.filter(deleted_at__isnull=True).order_by("-id")
        paginator = Paginator(queryset, per_page)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj

    def search_patients(self, params: Dict[str, Any]):
        per_page_raw = params.get("per_page", 30)
        search_term = (params.get("search") or params.get("q") or "").strip()
        try:
            per_page = int(per_page_raw)
        except (TypeError, ValueError):
            per_page = 30

        queryset = Patient.objects.filter(deleted_at__isnull=True).order_by("-id")
        if search_term:
            queryset = queryset.annotate(
                paternal_name=Concat("paternal_lastname", Value(" "), "name"),
                #full_name=Concat("name", Value(" "), "paternal_lastname", Value(" "), "maternal_lastname"),
                paternal_maternal_name=Concat("paternal_lastname", Value(" "), "maternal_lastname", Value(" "), "name"),
            ).filter(
                Q(document_number__iexact=search_term)
                | Q(document_number__istartswith=search_term)
                | Q(name__istartswith=search_term)
                | Q(name__icontains=search_term)
                | Q(paternal_lastname__istartswith=search_term)
                | Q(paternal_lastname__icontains=search_term)
                | Q(maternal_lastname__istartswith=search_term)
                | Q(maternal_lastname__icontains=search_term)
                | Q(paternal_name__istartswith=search_term)
                #| Q(full_name__istartswith=search_term)
                | Q(paternal_maternal_name__istartswith=search_term)
            )

        paginator = Paginator(queryset, per_page)
        try:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj

    # ---------- helpers ----------
    @staticmethod
    def _id_or_none(obj_or_id):
        """Devuelve el ID si recibe una instancia o un int/str. None si viene vac  o."""
        if obj_or_id is None:
            return None
        # instancias de modelos
        if isinstance(obj_or_id, (Region, Province, District)):
            return obj_or_id.id
        # enteros o strings de d  gitos
        if isinstance(obj_or_id, int):
            return obj_or_id
        if isinstance(obj_or_id, str) and obj_or_id.isdigit():
            return int(obj_or_id)
        return obj_or_id  #   ltimo recurso: devu  lvelo tal cual

    @staticmethod
    def _validate_geo(region_id: Any, province_id: Any, district_id: Any):
        """Valida que province pertenezca a region y district a province. Lanza ValidationError (400)."""
        rid = PatientService._id_or_none(region_id)
        pid = PatientService._id_or_none(province_id)
        did = PatientService._id_or_none(district_id)

        # si no hay alguno, no validamos jerarqu  a (permite parciales)
        if not (rid and pid):
            return
        province = Province.objects.filter(id=pid).first()
        if not province or province.region_id != rid:
            raise ValidationError({"province": "La provincia seleccionada no pertenece a la regi  n indicada."})

        if did:
            district = District.objects.filter(id=did).first()
            if not district or district.province_id != pid:
                raise ValidationError({"district": "El distrito seleccionado no pertenece a la provincia indicada."})

    # ---------- operaciones ----------
    @transaction.atomic
    def store_or_restore(self, data: Dict[str, Any]) -> Tuple[Patient, bool, bool]:
        # validaci  n geogr  fica (acepta id o instancia en data)
        self._validate_geo(data.get("region"), data.get("province"), data.get("district"))

        patient = Patient.objects.create(**data)
        return patient, True, False

    @transaction.atomic
    def update(self, patient: Patient, data: Dict[str, Any]) -> Patient:
        # si se tocan FKs de geo, validar coherencia
        if any(k in data for k in ("region", "province", "district")):
            region_val = data.get("region", patient.region_id)
            province_val = data.get("province", patient.province_id)
            district_val = data.get("district", patient.district_id)
            self._validate_geo(region_val, province_val, district_val)

        changed_fields = []
        for field, value in data.items():
            if not hasattr(patient, field):
                continue
            current = getattr(patient, field)
            # compara por ID si son FKs, para evitar falsos cambios por __str__
            if hasattr(current, "id"):
                cur_val = current.id
            else:
                cur_val = current
            new_val = value.id if hasattr(value, "id") else value
            if cur_val != new_val:
                setattr(patient, field, value)
                changed_fields.append(field)

        if changed_fields:
            patient.save(update_fields=changed_fields)
        return patient

    @transaction.atomic
    def destroy(self, patient: Patient) -> None:
        patient.soft_delete()

    def restore(self, patient_id: int) -> bool:
        try:
            patient = Patient.objects.get(id=patient_id, deleted_at__isnull=False)
            patient.restore()
            return True
        except Patient.DoesNotExist:
            return False