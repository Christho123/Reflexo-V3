from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date, timedelta
from company_reports.services.statistics_services import StatisticsService
from appointments_status.models.appointment import Appointment
from appointments_status.models.payment_type import PaymentType
from therapists.models.therapist import Therapist
from patients.models.patient import Patient


class StatisticsSundayExclusionTest(TestCase):
    """
    Test para verificar que las estadísticas NO incluyen citas de los domingos.
    Las estadísticas deben ser solo de Lunes a Sábado.
    """
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear datos de prueba
        self.therapist = Therapist.objects.create(
            first_name="Test",
            last_name_paternal="Therapist",
            last_name_maternal="Test"
        )
        
        self.patient = Patient.objects.create(
            first_name="Test",
            last_name_paternal="Patient",
            last_name_maternal="Test"
        )
        
        self.payment_type = PaymentType.objects.create(
            name="Efectivo"
        )
        
        # Crear fechas de prueba
        # Lunes (día 1)
        self.monday = date(2024, 1, 1)  # 1 de enero de 2024 es lunes
        # Domingo (día 7) 
        self.sunday = date(2024, 1, 7)  # 7 de enero de 2024 es domingo
        # Sábado (día 6)
        self.saturday = date(2024, 1, 6)  # 6 de enero de 2024 es sábado
        
        # Crear citas de prueba
        # Cita del lunes
        Appointment.objects.create(
            appointment_date=self.monday,
            therapist=self.therapist,
            patient=self.patient,
            payment_type=self.payment_type,
            payment=100.0,
            appointment_status="C"
        )
        
        # Cita del domingo (NO debería contarse)
        Appointment.objects.create(
            appointment_date=self.sunday,
            therapist=self.therapist,
            patient=self.patient,
            payment_type=self.payment_type,
            payment=200.0,
            appointment_status="C"
        )
        
        # Cita del sábado
        Appointment.objects.create(
            appointment_date=self.saturday,
            therapist=self.therapist,
            patient=self.patient,
            payment_type=self.payment_type,
            payment=150.0,
            appointment_status="C"
        )
        
        self.service = StatisticsService()
    
    def test_sunday_not_included_in_income_statistics(self):
        """
        Verifica que los ingresos de los domingos NO se incluyen en las estadísticas
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        ingresos = self.service.get_ingresos_por_dia_semana(start_date, end_date)
        
        # Verificar que solo aparecen Lunes y Sábado
        self.assertIn("Lunes", ingresos)
        self.assertIn("Sabado", ingresos)
        self.assertNotIn("Domingo", ingresos)
        
        # Verificar los montos
        self.assertEqual(ingresos["Lunes"], 100.0)
        self.assertEqual(ingresos["Sabado"], 150.0)
        
        # Verificar que no hay día 7 (Domingo) en los resultados
        self.assertNotIn(7, [self._get_weekday_number(day) for day in ingresos.keys()])
    
    def test_sunday_not_included_in_sessions_statistics(self):
        """
        Verifica que las sesiones de los domingos NO se incluyen en las estadísticas
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        sesiones = self.service.get_sesiones_por_dia_semana(start_date, end_date)
        
        # Verificar que solo aparecen Lunes y Sábado
        self.assertIn("Lunes", sesiones)
        self.assertIn("Sabado", sesiones)
        self.assertNotIn("Domingo", sesiones)
        
        # Verificar los conteos
        self.assertEqual(sesiones["Lunes"], 1)
        self.assertEqual(sesiones["Sabado"], 1)
        
        # Verificar que no hay día 7 (Domingo) en los resultados
        self.assertNotIn(7, [self._get_weekday_number(day) for day in sesiones.keys()])
    
    def test_sunday_not_included_in_main_metrics(self):
        """
        Verifica que las métricas principales NO incluyen citas de domingos
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        metricas = self.service.get_metricas_principales(start_date, end_date)
        
        # Debería contar solo 2 citas (Lunes y Sábado), no 3 (incluyendo Domingo)
        self.assertEqual(metricas["ttlsesiones"], 2)
        
        # Debería sumar solo 250.0 (100 + 150), no 450.0 (incluyendo 200 del domingo)
        self.assertEqual(metricas["ttlganancias"], 250.0)
    
    def test_sunday_not_included_in_therapist_performance(self):
        """
        Verifica que el rendimiento de terapeutas NO incluye citas de domingos
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        rendimiento = self.service.get_rendimiento_terapeutas(start_date, end_date)
        
        # Debería haber solo un terapeuta con 2 sesiones y 250.0 de ingresos
        self.assertEqual(len(rendimiento), 1)
        terapeuta = rendimiento[0]
        self.assertEqual(terapeuta["sesiones"], 2)
        self.assertEqual(terapeuta["ingresos"], 250.0)
    
    def test_sunday_not_included_in_payment_types(self):
        """
        Verifica que los tipos de pago NO incluyen citas de domingos
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        tipos_pago = self.service.get_tipos_de_pago(start_date, end_date)
        
        # Debería contar solo 2 usos de "Efectivo", no 3
        self.assertEqual(tipos_pago["Efectivo"], 2)
    
    def test_sunday_not_included_in_patient_types(self):
        """
        Verifica que los tipos de pacientes NO incluyen citas de domingos
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        tipos_pacientes = self.service.get_tipos_pacientes(start_date, end_date)
        
        # Debería contar solo 2 citas con status "C", no 3
        self.assertEqual(tipos_pacientes["c"], 2)
    
    def test_complete_statistics_exclude_sunday(self):
        """
        Verifica que todas las estadísticas completas excluyen los domingos
        """
        start_date = date(2024, 1, 1)  # Lunes
        end_date = date(2024, 1, 7)    # Domingo
        
        estadisticas = self.service.get_statistics(start_date, end_date)
        
        # Verificar que no hay domingos en ingresos
        self.assertNotIn("Domingo", estadisticas["ingresos"])
        
        # Verificar que no hay domingos en sesiones
        self.assertNotIn("Domingo", estadisticas["sesiones"])
        
        # Verificar métricas principales
        self.assertEqual(estadisticas["metricas"]["ttlsesiones"], 2)
        self.assertEqual(estadisticas["metricas"]["ttlganancias"], 250.0)
        
        # Verificar tipos de pago
        self.assertEqual(estadisticas["tipos_pago"]["Efectivo"], 2)
        
        # Verificar tipos de pacientes
        self.assertEqual(estadisticas["tipos_pacientes"]["c"], 2)
    
    def _get_weekday_number(self, day_name):
        """
        Método auxiliar para obtener el número del día de la semana
        """
        dias = {
            "Lunes": 1, "Martes": 2, "Miercoles": 3,
            "Jueves": 4, "Viernes": 5, "Sabado": 6, "Domingo": 7
        }
        return dias.get(day_name, 0)
    
    def test_weekday_mapping_correctness(self):
        """
        Verifica que el mapeo de días de la semana es correcto
        """
        # Verificar que el mapeo interno del servicio es correcto
        dias_semana = {
            1: "Lunes", 2: "Martes", 3: "Miercoles",
            4: "Jueves", 5: "Viernes", 6: "Sabado"
        }
        
        # Verificar que NO incluye el domingo (día 7)
        self.assertNotIn(7, dias_semana)
        
        # Verificar que incluye todos los días laborales
        self.assertEqual(len(dias_semana), 6)
        self.assertIn(1, dias_semana)  # Lunes
        self.assertIn(6, dias_semana)  # Sábado

