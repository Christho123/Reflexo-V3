from datetime import datetime
from django.utils.timezone import localtime
from django.db.models import Count, Q, CharField, Value, Sum
from django.db.models.functions import Concat, TruncDate
from appointments_status.models.appointment import Appointment
from appointments_status.models.ticket import Ticket
from therapists.models.therapist import Therapist


# from django.db import models  # 👈 no se usa

class ReportService:
    def get_appointments_count_by_therapist(self, validated_data):
        """
        Conteo de TODAS las citas por terapeuta para una fecha dada.
        Agrupa desde Appointment para evitar problemas de related_name.
        """
        query_date = validated_data.get("date")

        # Si appointment_date es DateField, basta con igualdad.
        # Si es DateTimeField, usamos TruncDate para comparar el día.
        # Esta versión funciona en ambos casos (TruncDate ⇒ date-only).
        qs = (
            Appointment.objects
            .filter(therapist__isnull=False)
            .annotate(day=TruncDate("appointment_date"))
            .filter(day=query_date)
            .values(
                "therapist_id",
                "therapist__first_name",
                "therapist__last_name_paternal",
                "therapist__last_name_maternal",
            )
            .annotate(appointments_count=Count("id"))
        )

        therapists = [
            {
                "id": row["therapist_id"],
                "name": f'{row["therapist__first_name"]} {row["therapist__last_name_paternal"] or ""} {row["therapist__last_name_maternal"] or ""}'.strip(),
                "last_name_paternal": row["therapist__last_name_paternal"],
                "last_name_maternal": row["therapist__last_name_maternal"],
                "appointments_count": row["appointments_count"],
            }
            for row in qs
        ]

        # Ordenar por mayor número de citas (como antes)
        therapists.sort(key=lambda t: (-t["appointments_count"], t["last_name_paternal"] or "", t["last_name_maternal"] or "", t["id"]))

        total_appointments = sum(t["appointments_count"] for t in therapists)

        return {
            "therapists_appointments": therapists,
            "total_appointments_count": total_appointments,
        }

    def get_patients_by_therapist(self, validated_data):
        """Pacientes agrupados por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")

        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .annotate(day=TruncDate("appointment_date"))
            .filter(day=query_date)
        )

        report = {}
        sin_terapeuta = {
            "therapist_id": "",
            "therapist": "Sin terapeuta asignado",
            "patients": {}
        }

        for appointment in appointments:
            patient = appointment.patient
            therapist = appointment.therapist
            if not patient:
                continue

            patient_data = {
                "patient_id": patient.id,
                "patient": f"{patient.paternal_lastname} {patient.maternal_lastname or ''} {patient.name}".strip(),
                "appointments": 0,
            }

            if not therapist:
                key = patient.id
                if key not in sin_terapeuta["patients"]:
                    sin_terapeuta["patients"][key] = patient_data
                sin_terapeuta["patients"][key]["appointments"] += 1
            else:
                t_id = therapist.id
                if t_id not in report:
                    report[t_id] = {
                        "therapist_id": t_id,
                        # usa first_name (no existe 'name' en el modelo)
                        "therapist": f"{therapist.last_name_paternal} {therapist.last_name_maternal or ''} {therapist.first_name}".strip(),
                        "patients": {}
                    }
                key = patient.id
                if key not in report[t_id]["patients"]:
                    report[t_id]["patients"][key] = patient_data
                report[t_id]["patients"][key]["appointments"] += 1

        # Agregar grupo "sin terapeuta" si aplica
        if sin_terapeuta["patients"]:
            report["sinTherapist"] = sin_terapeuta

        # Convertir dicts de pacientes a listas
        for therapist_id in list(report.keys()):
            report[therapist_id]["patients"] = list(report[therapist_id]["patients"].values())

        return list(report.values())

    def get_daily_cash(self, validated_data):
        """Resumen diario de efectivo detallado por cita."""
        from appointments_status.models import Ticket
        query_date = validated_data.get("date")

        # Buscar citas con pagos directos
        direct_payments = (
            Appointment.objects
            .filter(
                appointment_date=query_date,
                payment__isnull=False,
                payment_type__isnull=False
            )
            .values(
                'id',
                'payment',
                'payment_type',
                'payment_type__name'
            )
            .order_by('-id')
        )

        # Buscar tickets pagados para citas del día
        ticket_payments = (
            Ticket.objects
            .filter(
                payment_date__date=query_date,
                status='paid',
                is_active=True
            )
            .select_related('appointment', 'payment_type')
            .values(
                'appointment__id',
                'amount',
                'payment_type',
                'payment_type__name'
            )
            .order_by('-payment_date')
        )

        result = []
        
        # Procesar pagos directos de citas
        for p in direct_payments:
            result.append({
                "id_cita": p['id'],
                "payment": p['payment'],
                "payment_type": p['payment_type'],
                "payment_type_name": p['payment_type__name']
            })

        # Procesar pagos a través de tickets
        for t in ticket_payments:
            result.append({
                "id_cita": t['appointment__id'],
                "payment": t['amount'],
                "payment_type": t['payment_type'],
                "payment_type_name": t['payment_type__name']
            })

        return result

    def get_improved_daily_cash(self, validated_data):
        """
        Reporte mejorado de caja chica con información detallada de pagos.
        Incluye resumen por tipo de pago y totales.
        """
        query_date = validated_data.get("date")

        # Obtener pagos de citas
        appointment_payments = (
            Appointment.objects
            .filter(
                appointment_date__date=query_date,
                payment__isnull=False,
                payment__gt=0
            )
            .select_related('payment_type', 'patient', 'therapist')
            .values(
                'id',
                'payment',
                'payment_type__name',
                'patient__name',
                'patient__paternal_lastname',
                'patient__maternal_lastname',
                'therapist__first_name',
                'therapist__last_name_paternal',
                'therapist__last_name_maternal',
                'ticket_number'
            )
            .order_by('-payment')
        )

        # Obtener pagos de tickets
        ticket_payments = (
            Ticket.objects
            .filter(
                payment_date__date=query_date,
                status='paid',
                amount__gt=0
            )
            .select_related('appointment__patient', 'appointment__therapist')
            .values(
                'id',
                'amount',
                'payment_method',
                'ticket_number',
                'appointment__patient__name',
                'appointment__patient__paternal_lastname',
                'appointment__patient__maternal_lastname',
                'appointment__therapist__first_name',
                'appointment__therapist__last_name_paternal',
                'appointment__therapist__last_name_maternal'
            )
            .order_by('-amount')
        )

        # Procesar pagos de citas
        appointment_data = []
        for payment in appointment_payments:
            patient_name = f"{payment['patient__paternal_lastname'] or ''} {payment['patient__maternal_lastname'] or ''} {payment['patient__name'] or ''}".strip()
            therapist_name = f"{payment['therapist__last_name_paternal'] or ''} {payment['therapist__last_name_maternal'] or ''} {payment['therapist__first_name'] or ''}".strip()
            
            appointment_data.append({
                "tipo": "Cita",
                "id": payment['id'],
                "ticket_number": payment['ticket_number'] or f"CITA-{payment['id']}",
                "monto": float(payment['payment']),
                "metodo_pago": payment['payment_type__name'] or "No especificado",
                "paciente": patient_name,
                "terapeuta": therapist_name,
                "fecha_pago": query_date.strftime("%Y-%m-%d")
            })

        # Procesar pagos de tickets
        ticket_data = []
        for payment in ticket_payments:
            patient_name = f"{payment['appointment__patient__paternal_lastname'] or ''} {payment['appointment__patient__maternal_lastname'] or ''} {payment['appointment__patient__name'] or ''}".strip()
            therapist_name = f"{payment['appointment__therapist__last_name_paternal'] or ''} {payment['appointment__therapist__last_name_maternal'] or ''} {payment['appointment__therapist__first_name'] or ''}".strip()
            
            ticket_data.append({
                "tipo": "Ticket",
                "id": payment['id'],
                "ticket_number": payment['ticket_number'],
                "monto": float(payment['amount']),
                "metodo_pago": payment['payment_method'],
                "paciente": patient_name,
                "terapeuta": therapist_name,
                "fecha_pago": query_date.strftime("%Y-%m-%d")
            })

        # Combinar todos los pagos
        all_payments = appointment_data + ticket_data
        
        # Calcular totales por método de pago
        payment_summary = {}
        total_general = 0
        
        for payment in all_payments:
            metodo = payment['metodo_pago']
            monto = payment['monto']
            
            if metodo not in payment_summary:
                payment_summary[metodo] = {
                    'metodo': metodo,
                    'cantidad_pagos': 0,
                    'total': 0.0
                }
            
            payment_summary[metodo]['cantidad_pagos'] += 1
            payment_summary[metodo]['total'] += monto
            total_general += monto

        # Convertir a lista y ordenar por total
        payment_summary_list = list(payment_summary.values())
        payment_summary_list.sort(key=lambda x: x['total'], reverse=True)

        return {
            "fecha": query_date.strftime("%Y-%m-%d"),
            "pagos_detallados": all_payments,
            "resumen_por_metodo": payment_summary_list,
            "total_general": round(total_general, 2),
            "cantidad_total_pagos": len(all_payments)
        }

    def get_daily_paid_tickets(self, validated_data):
        """
        Reporte diario de todos los tickets PAGADOS.
        Incluye información detallada de cada ticket pagado.
        """
        query_date = validated_data.get("date")

        # Obtener tickets pagados del día
        paid_tickets = (
            Ticket.objects
            .filter(
                payment_date__date=query_date,
                status='paid',
                is_active=True
            )
            .select_related(
                'appointment__patient',
                'appointment__therapist',
                'appointment__payment_type',
                'payment_type'
            )
            .values(
                'id',
                'ticket_number',
                'amount',
                'payment_type',
                'payment_type__name',
                'payment_date',
                'description',
                'appointment__id',
                'appointment__appointment_date',
                'appointment__hour',
                'appointment__room',
                'appointment__payment_type__name',
                'appointment__patient__name',
                'appointment__patient__paternal_lastname',
                'appointment__patient__maternal_lastname',
                'appointment__patient__document_number',
                'appointment__patient__phone1',
                'appointment__therapist__first_name',
                'appointment__therapist__last_name_paternal',
                'appointment__therapist__last_name_maternal',
                'appointment__therapist__document_number'
            )
            .order_by('-payment_date')
        )

        # Procesar tickets pagados
        tickets_data = []
        total_amount = 0.0
        
        for ticket in paid_tickets:
            # Formatear nombre del paciente
            patient_name = f"{ticket['appointment__patient__paternal_lastname'] or ''} {ticket['appointment__patient__maternal_lastname'] or ''} {ticket['appointment__patient__name'] or ''}".strip()
            
            # Formatear nombre del terapeuta
            therapist_name = f"{ticket['appointment__therapist__last_name_paternal'] or ''} {ticket['appointment__therapist__last_name_maternal'] or ''} {ticket['appointment__therapist__first_name'] or ''}".strip()
            
            # Formatear fecha y hora de la cita
            appointment_datetime = ticket['appointment__appointment_date']
            appointment_date = appointment_datetime.strftime("%Y-%m-%d") if appointment_datetime else "No programada"
            appointment_time = ticket['appointment__hour'].strftime("%H:%M") if ticket['appointment__hour'] else "No especificada"
            
            # Formatear fecha de pago
            payment_datetime = ticket['payment_date']
            payment_date = payment_datetime.strftime("%Y-%m-%d %H:%M") if payment_datetime else "No especificada"
            
            ticket_info = {
                "ticket_id": ticket['id'],
                "numero_ticket": ticket['ticket_number'],
                "monto": float(ticket['amount']),
                "metodo_pago": ticket['payment_type__name'] or "No especificado",
                "fecha_pago": payment_date,
                "descripcion": ticket['description'] or "Sin descripción",
                
                # Información de la cita
                "cita_id": ticket['appointment__id'],
                "fecha_cita": appointment_date,
                "hora_cita": appointment_time,
                "consultorio": ticket['appointment__room'] or "No especificado",
                "tipo_pago_cita": ticket['appointment__payment_type__name'] or "No especificado",
                
                # Información del paciente
                "paciente_nombre": patient_name,
                "paciente_documento": ticket['appointment__patient__document_number'] or "No especificado",
                "paciente_telefono": ticket['appointment__patient__phone1'] or "No especificado",
                
                # Información del terapeuta
                "terapeuta_nombre": therapist_name,
                "terapeuta_documento": ticket['appointment__therapist__document_number'] or "No especificado"
            }
            
            tickets_data.append(ticket_info)
            total_amount += float(ticket['amount'])

        # Calcular resumen por método de pago
        payment_methods_summary = {}
        for ticket in tickets_data:
            metodo = ticket['metodo_pago']
            monto = ticket['monto']
            
            if metodo not in payment_methods_summary:
                payment_methods_summary[metodo] = {
                    'metodo': metodo,
                    'cantidad_tickets': 0,
                    'total': 0.0
                }
            
            payment_methods_summary[metodo]['cantidad_tickets'] += 1
            payment_methods_summary[metodo]['total'] += monto

        # Convertir a lista y ordenar por total
        payment_methods_list = list(payment_methods_summary.values())
        payment_methods_list.sort(key=lambda x: x['total'], reverse=True)

        return {
            "fecha": query_date.strftime("%Y-%m-%d"),
            "tickets_pagados": tickets_data,
            "resumen_por_metodo": payment_methods_list,
            "total_general": round(total_amount, 2),
            "cantidad_tickets": len(tickets_data),
            "metodos_pago_utilizados": list(payment_methods_summary.keys())
        }

    def get_appointments_between_dates(self, validated_data):
        """Citas entre dos fechas dadas."""
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")

        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .filter(
                appointment_date__gte=start_date,
                appointment_date__lte=end_date
            )
            .order_by("appointment_date", "hour")
        )

        result = []
        for app in appointments:
            if not app.patient:
                continue

            patient_name = " ".join(filter(None, [
                app.patient.paternal_lastname,
                app.patient.maternal_lastname,
                app.patient.name
            ]))

            hour_val = app.hour
            hour_str = hour_val if isinstance(hour_val, str) else (hour_val.strftime("%H:%M") if hour_val else "")

            result.append({
                "appointment_id": app.id,
                "patient_id": app.patient.id,
                "document_number_patient": app.patient.document_number,
                "patient": patient_name,
                "phone1_patient": app.patient.phone1,
                "appointment_date": app.appointment_date.strftime("%Y-%m-%d"),
                "hour": hour_str,
            })

        return result
