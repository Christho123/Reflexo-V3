from django.db.models import Count, Sum, Avg, Q, Case, When, F, Value
from django.db.models.functions import ExtractWeekDay, Concat
from django.utils import timezone
from appointments_status.models.appointment import Appointment

class StatisticsService:
    def get_metricas_principales(self, start, end):
        return Appointment.objects.filter(
            appointment_date__range=[start, end]
        ).aggregate(
            ttlpacientes=Count("patient", distinct=True),
            ttlsesiones=Count("id"),
            ttlganancias=Sum("payment")
        )

    def get_tipos_de_pago(self, start, end):
        pagos = (
            Appointment.objects
            .filter(
                appointment_date__range=[start, end]
            )
            .values("payment_type__name")
            .annotate(usos=Count("id"))
        )
        return {(p["payment_type__name"] or "Sin tipo"): p["usos"] for p in pagos}

    def get_rendimiento_terapeutas(self, start, end):
        # 1. Consulta base: sesiones e ingresos por terapeuta 
        stats = list(
            Appointment.objects
            .filter(
                appointment_date__range=[start, end]
            )
            .values("therapist__id", "hour")
            .annotate(
                # Formato de nombre  "Apellido1 Apellido2, Nombre"
                terapeuta=Concat(
                    'therapist__last_name_paternal',
                    Value(' '),
                    'therapist__last_name_maternal', 
                    Value(', '),
                    'therapist__first_name'
                ),
                sesiones=Count("id"),
                ingresos=Sum("payment")
            )
            .order_by("therapist__id", "hour")
        )
        
        # Agrupar las citas por terapeuta para recolectar las horas
        terapeutas_agrupados = {}
        for stat in stats:
            therapist_id = stat["therapist__id"]
            if therapist_id not in terapeutas_agrupados:
                terapeutas_agrupados[therapist_id] = {
                    "id": therapist_id,
                    "terapeuta": stat['terapeuta'] or "Sin nombre",
                    "sesiones": 0,
                    "ingresos": 0.0,
                    "raiting_original": 0.0,
                    "horas_citas": []
                }
            terapeutas_agrupados[therapist_id]["sesiones"] += 1
            terapeutas_agrupados[therapist_id]["ingresos"] += float(stat['ingresos'] or 0)
            if stat["hour"]:
                terapeutas_agrupados[therapist_id]["horas_citas"].append(stat["hour"].strftime("%H:%M"))

        stats_final = list(terapeutas_agrupados.values())

        if not stats_final:
            return []

        # 2. Calculamos promedios globales
        total_sesiones = sum(s['sesiones'] for s in stats_final)
        total_ingresos = sum(float(s['ingresos'] or 0) for s in stats_final)
        num_terapeutas = len(stats_final)
        
        prom_sesiones = total_sesiones / num_terapeutas if num_terapeutas > 0 else 1.0
        prom_ingresos = total_ingresos / num_terapeutas if num_terapeutas > 0 else 1.0
        
        # 3. Calcular rating original para cada terapeuta
        for stat in stats_final:
            sesiones = stat['sesiones']
            ingresos = float(stat['ingresos'] or 0)  
            
            # Fórmula 70% sesiones, 30% ingresos
            rating_original = 0.0
            if prom_sesiones > 0 and prom_ingresos > 0:
                rating_original = (sesiones / prom_sesiones) * 0.7 + (ingresos / prom_ingresos) * 0.3
            elif prom_sesiones > 0:
                rating_original = (sesiones / prom_sesiones) * 0.7
            elif prom_ingresos > 0:
                rating_original = (ingresos / prom_ingresos) * 0.3
                
            stat['raiting_original'] = rating_original
        
        # 4. Encontrar el máximo rating original
        max_original = max(s['raiting_original'] for s in stats_final) if stats_final else 1.0
        
        # 5. Escalar a 5 puntos y formatear resultado
        resultado = []
        for stat in stats_final:
            scaled_rating = (stat['raiting_original'] / max_original) * 5
            
            resultado.append({
                "id": stat["id"],
                "terapeuta": stat['terapeuta'],
                "sesiones": stat["sesiones"],
                "ingresos": float(stat["ingresos"]) if stat["ingresos"] else 0.0,
                "raiting": round(scaled_rating, 2),
                "horas_citas": stat["horas_citas"]
            })
        
        return resultado

    def get_ingresos_por_dia_semana(self, start, end):
        
        dias_semana = {      
            2: "Lunes",      
            3: "Martes",     
            4: "Miercoles",   
            5: "Jueves",    
            6: "Viernes",      
            7: "Sabado"     
        }
        
        ingresos_raw = (
            Appointment.objects
            .filter(
                appointment_date__range=[start, end]
            )
            .annotate(dia_semana=ExtractWeekDay("appointment_date"))
            .filter(dia_semana__lte=6)  # Excluir domingo (día 7)
            .values("dia_semana")
            .annotate(total=Sum("payment"))  
            .order_by("dia_semana")
        )
        
        
        resultado = {}
        for item in ingresos_raw:
            dia_nombre = dias_semana.get(item["dia_semana"], f"Día {item['dia_semana']}")
            resultado[dia_nombre] = float(item["total"]) if item["total"] else 0.0
        
        return resultado

    def get_sesiones_por_dia_semana(self, start, end):
        dias_semana = {
            2: "Lunes", 3: "Martes", 4: "Miercoles",
            5: "Jueves", 6: "Viernes", 7: "Sabado"
        }
        
        sesiones_raw = (
            Appointment.objects
            .filter(
                appointment_date__range=[start, end]
            )
            .annotate(dia_semana=ExtractWeekDay("appointment_date"))
            .filter(dia_semana__lte=6)  # Excluir domingo (día 7)
            .values("dia_semana")
            .annotate(sesiones=Count("id"))
            .order_by("dia_semana")
        )
        
        resultado = {}
        for item in sesiones_raw:
            dia_nombre = dias_semana.get(item["dia_semana"], f"Día {item['dia_semana']}")
            resultado[dia_nombre] = item["sesiones"]
        
        return resultado

    def get_tipos_pacientes(self, start, end):
        return Appointment.objects.filter(
            appointment_date__range=[start, end]
        ).aggregate(
            c=Count("id", filter=Q(appointment_status__name__iexact="C")),
            cc=Count("id", filter=Q(appointment_status__name__iexact="CC"))
        )

    def get_statistics(self, start, end):
        return {
            "terapeutas": self.get_rendimiento_terapeutas(start, end),
            "tipos_pago": self.get_tipos_de_pago(start, end),
            "metricas": self.get_metricas_principales(start, end),
            "ingresos": self.get_ingresos_por_dia_semana(start, end),
            "sesiones": self.get_sesiones_por_dia_semana(start, end),
            "tipos_pacientes": self.get_tipos_pacientes(start, end),
        }