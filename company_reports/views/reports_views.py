from django.http import JsonResponse, HttpResponse
from company_reports.services.reports_services import ReportService
from company_reports.serialiazers.reports_serializers import (
    DateParameterSerializer,
    TherapistAppointmentSerializer,
    PatientByTherapistSerializer,
    DailyCashSerializer,
    AppointmentRangeSerializer,
    PDFContextSerializer,
    ImprovedDailyCashSerializer,
    DailyPaidTicketsSerializer,
)
from django.shortcuts import render
# from django_xhtml2pdf.utils import pdf_decorator
from django.views.decorators.csrf import csrf_exempt
import xlsxwriter
import io
import json

report_service = ReportService()


# --------- Helpers ---------
def _merge_params(request):
    """
    Mezcla query params y body (JSON o form) para soportar GET y POST.
    - Los valores del body tienen prioridad sobre los de la query string.
    """
    merged = {}

    # Query params
    for k, v in request.GET.items():
        merged[k] = v

    # Body (POST/PUT/PATCH)
    if request.method in ("POST", "PUT", "PATCH"):
        if request.content_type and "application/json" in request.content_type:
            try:
                body = json.loads(request.body or b"{}")
                if isinstance(body, dict):
                    merged.update(body)
            except json.JSONDecodeError:
                pass
        else:
            for k, v in request.POST.items():
                merged[k] = v

    return merged


# ===========================
#   JSON API
# ===========================
class ReportAPIView:
    """Responsable exclusivamente de endpoints JSON de reportes."""

    @staticmethod
    def get_number_appointments_per_therapist(request):
        """
        Devuelve JSON con el número de citas por terapeuta para una fecha dada.
        GET  /...?date=YYYY-MM-DD
        POST /... con body {"date":"YYYY-MM-DD"} o ?date=...
        """
        # Validar parámetros (mezcla GET + body)
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        # Obtener datos usando parámetros validados
        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Serializar respuesta (con porcentaje)
        response_serializer = TherapistAppointmentSerializer(
            data["therapists_appointments"],
            many=True,
            context={"total_appointments": data["total_appointments_count"]},
        )

        return JsonResponse(
            {
                "date": str(serializer.validated_data.get("date")),
                "therapists_appointments": response_serializer.data,
                "total_appointments_count": data["total_appointments_count"],
            }
        )

    @staticmethod
    def get_patients_by_therapist(request):
        """Devuelve JSON con los pacientes agrupados por terapeuta para una fecha dada."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = PatientByTherapistSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_daily_cash(request):
        """Devuelve JSON con el resumen diario de efectivo agrupado por tipo de pago."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = DailyCashSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_improved_daily_cash(request):
        """Devuelve JSON con el reporte mejorado de caja chica."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_improved_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = ImprovedDailyCashSerializer(data)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_daily_paid_tickets(request):
        """Devuelve JSON con el reporte diario de todos los tickets PAGADOS."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_paid_tickets(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = DailyPaidTicketsSerializer(data)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_appointments_between_dates(request):
        """Devuelve JSON con todas las citas entre dos fechas con info de paciente y terapeuta."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = AppointmentRangeSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)


# ===========================
#   PDF
# ===========================
class PDFExportView:
    """Responsable exclusivamente de la generación de PDFs."""

    @staticmethod
    # @pdf_decorator(pdfname="citas_terapeuta.pdf")
    def pdf_citas_terapeuta(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Citas por Terapeuta",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/citas_terapeuta.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="pacientes_por_terapeuta.pdf")
    def pdf_pacientes_terapeuta(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Pacientes por Terapeuta",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/pacientes_terapeuta.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="resumen_caja.pdf")
    def pdf_resumen_caja(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Calcular total correcto (sumando 'payment')
        total = sum(float(item.get("payment", 0) or 0) for item in data) if data else 0.0

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "total": total,
            "title": "Resumen de Caja Diaria",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/resumen_caja.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="caja_chica_mejorada.pdf")
    def pdf_caja_chica_mejorada(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_improved_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Reporte Mejorado de Caja Chica",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/caja_chica_mejorada.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="tickets_pagados.pdf")
    def pdf_tickets_pagados(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_paid_tickets(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Reporte Diario de Tickets Pagados",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/tickets_pagados.html", context)


# ===========================
#   Excel
# ===========================
class ExcelExportView:
    """Responsable exclusivamente de la exportación a Excel."""

    @staticmethod
    def exportar_excel_citas(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Citas")

        # Formato encabezado
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#2c3e50", "font_color": "white", "border": 1}
        )

        # Encabezados alineados con AppointmentRangeSerializer
        headers = [
            "ID Paciente",
            "DNI/Documento",
            "Paciente",
            "Teléfono",
            "Fecha",
            "Hora",
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Escribir datos
        for row, appointment in enumerate(data, start=1):
            worksheet.write(row, 0, appointment.get("patient_id", ""))
            worksheet.write(row, 1, appointment.get("document_number_patient", ""))
            worksheet.write(row, 2, appointment.get("patient", ""))
            worksheet.write(row, 3, appointment.get("phone1_patient", ""))
            worksheet.write(row, 4, appointment.get("appointment_date", ""))
            worksheet.write(row, 5, appointment.get("hour", ""))

        # Anchos de columna
        worksheet.set_column("A:A", 12)
        worksheet.set_column("B:B", 15)
        worksheet.set_column("C:C", 40)
        worksheet.set_column("D:D", 15)
        worksheet.set_column("E:E", 12)
        worksheet.set_column("F:F", 10)

        workbook.close()
        output.seek(0)

        # Nombre de archivo (si hay rango en query)
        start_date = serializer.validated_data.get("start_date")
        end_date = serializer.validated_data.get("end_date")
        if start_date and end_date:
            filename = f"citas_{start_date}_a_{end_date}.xlsx"
        else:
            filename = "citas.xlsx"

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    @staticmethod
    def exportar_excel_caja_chica_mejorada(request):
        """Exporta a Excel el reporte mejorado de caja chica."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_improved_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Caja Chica")

        # Formato encabezado
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#2c3e50", "font_color": "white", "border": 1}
        )

        # Encabezados para el reporte de caja chica
        headers = [
            "Tipo",
            "ID",
            "Número Ticket",
            "Monto",
            "Método Pago",
            "Paciente",
            "Terapeuta",
            "Fecha Pago",
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Escribir datos
        for row, payment in enumerate(data.get("pagos_detallados", []), start=1):
            worksheet.write(row, 0, payment.get("tipo", ""))
            worksheet.write(row, 1, payment.get("id", ""))
            worksheet.write(row, 2, payment.get("ticket_number", ""))
            worksheet.write(row, 3, payment.get("monto", 0))
            worksheet.write(row, 4, payment.get("metodo_pago", ""))
            worksheet.write(row, 5, payment.get("paciente", ""))
            worksheet.write(row, 6, payment.get("terapeuta", ""))
            worksheet.write(row, 7, payment.get("fecha_pago", ""))

        # Anchos de columna
        worksheet.set_column("A:A", 10)
        worksheet.set_column("B:B", 8)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 12)
        worksheet.set_column("E:E", 15)
        worksheet.set_column("F:F", 30)
        worksheet.set_column("G:G", 30)
        worksheet.set_column("H:H", 12)

        # Agregar resumen
        worksheet.write(len(data.get("pagos_detallados", [])) + 3, 0, "RESUMEN:", header_format)
        worksheet.write(len(data.get("pagos_detallados", [])) + 4, 0, "Total General:")
        worksheet.write(len(data.get("pagos_detallados", [])) + 4, 3, data.get("total_general", 0))

        workbook.close()
        output.seek(0)

        # Nombre de archivo
        date = serializer.validated_data.get("date")
        filename = f"caja_chica_mejorada_{date}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    @staticmethod
    def exportar_excel_tickets_pagados(request):
        """Exporta a Excel el reporte diario de tickets pagados."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_paid_tickets(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Tickets Pagados")

        # Formato encabezado
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#2c3e50", "font_color": "white", "border": 1}
        )

        # Encabezados para el reporte de tickets pagados
        headers = [
            "Número Ticket",
            "Monto",
            "Método Pago",
            "Fecha Pago",
            "Paciente",
            "Documento",
            "Teléfono",
            "Terapeuta",
            "Licencia",
            "Fecha Cita",
            "Hora Cita",
            "Consultorio",
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Escribir datos
        for row, ticket in enumerate(data.get("tickets_pagados", []), start=1):
            worksheet.write(row, 0, ticket.get("numero_ticket", ""))
            worksheet.write(row, 1, ticket.get("monto", 0))
            worksheet.write(row, 2, ticket.get("metodo_pago", ""))
            worksheet.write(row, 3, ticket.get("fecha_pago", ""))
            worksheet.write(row, 4, ticket.get("paciente_nombre", ""))
            worksheet.write(row, 5, ticket.get("paciente_documento", ""))
            worksheet.write(row, 6, ticket.get("paciente_telefono", ""))
            worksheet.write(row, 7, ticket.get("terapeuta_nombre", ""))
            worksheet.write(row, 8, ticket.get("terapeuta_licencia", ""))
            worksheet.write(row, 9, ticket.get("fecha_cita", ""))
            worksheet.write(row, 10, ticket.get("hora_cita", ""))
            worksheet.write(row, 11, ticket.get("consultorio", ""))

        # Anchos de columna
        worksheet.set_column("A:A", 20)  # Número Ticket
        worksheet.set_column("B:B", 12)  # Monto
        worksheet.set_column("C:C", 15)  # Método Pago
        worksheet.set_column("D:D", 18)  # Fecha Pago
        worksheet.set_column("E:E", 30)  # Paciente
        worksheet.set_column("F:F", 15)  # Documento
        worksheet.set_column("G:G", 15)  # Teléfono
        worksheet.set_column("H:H", 30)  # Terapeuta
        worksheet.set_column("I:I", 15)  # Licencia
        worksheet.set_column("J:J", 12)  # Fecha Cita
        worksheet.set_column("K:K", 10)  # Hora Cita
        worksheet.set_column("L:L", 12)  # Consultorio

        # Agregar resumen
        worksheet.write(len(data.get("tickets_pagados", [])) + 3, 0, "RESUMEN:", header_format)
        worksheet.write(len(data.get("tickets_pagados", [])) + 4, 0, "Total General:")
        worksheet.write(len(data.get("tickets_pagados", [])) + 4, 1, data.get("total_general", 0))
        worksheet.write(len(data.get("tickets_pagados", [])) + 5, 0, "Cantidad Tickets:")
        worksheet.write(len(data.get("tickets_pagados", [])) + 5, 1, data.get("cantidad_tickets", 0))

        workbook.close()
        output.seek(0)

        # Nombre de archivo
        date = serializer.validated_data.get("date")
        filename = f"tickets_pagados_{date}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


# ===========================
#   Wrappers (compatibilidad) + CSRF EXEMPT PARA TESTEAR POST EN POSTMAN
# ===========================
report_api = ReportAPIView()
pdf_export = PDFExportView()
excel_export = ExcelExportView()


@csrf_exempt
def get_number_appointments_per_therapist(request):
    try:
        return report_api.get_number_appointments_per_therapist(request)
    except Exception as e:
        import traceback

        print(f"Error en get_number_appointments_per_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_patients_by_therapist(request):
    try:
        return report_api.get_patients_by_therapist(request)
    except Exception as e:
        import traceback

        print(f"Error en get_patients_by_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_daily_cash(request):
    try:
        return report_api.get_daily_cash(request)
    except Exception as e:
        import traceback

        print(f"Error en get_daily_cash: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_improved_daily_cash(request):
    try:
        return report_api.get_improved_daily_cash(request)
    except Exception as e:
        import traceback

        print(f"Error en get_improved_daily_cash: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_daily_paid_tickets(request):
    try:
        return report_api.get_daily_paid_tickets(request)
    except Exception as e:
        import traceback

        print(f"Error en get_daily_paid_tickets: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_appointments_between_dates(request):
    try:
        return report_api.get_appointments_between_dates(request)
    except Exception as e:
        import traceback

        print(f"Error en get_appointments_between_dates: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


def reports_dashboard(request):
    return render(request, "reports.html")


def pdf_citas_terapeuta(request):
    return pdf_export.pdf_citas_terapeuta(request)


def pdf_pacientes_terapeuta(request):
    return pdf_export.pdf_pacientes_terapeuta(request)


def pdf_resumen_caja(request):
    return pdf_export.pdf_resumen_caja(request)


def pdf_caja_chica_mejorada(request):
    return pdf_export.pdf_caja_chica_mejorada(request)


def pdf_tickets_pagados(request):
    return pdf_export.pdf_tickets_pagados(request)


def exportar_excel_citas(request):
    return excel_export.exportar_excel_citas(request)


def exportar_excel_caja_chica_mejorada(request):
    return excel_export.exportar_excel_caja_chica_mejorada(request)


def exportar_excel_tickets_pagados(request):
    return excel_export.exportar_excel_tickets_pagados(request)
