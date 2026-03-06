from django.contrib import admin
from .models import Mecanicul, Operatie, Comanda


@admin.register(Mecanicul)
class MecaniculAdmin(admin.ModelAdmin):
    list_display = ("nume", "user")


@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ("client", "masina", "data_creare")


@admin.register(Operatie)
class OperatieAdmin(admin.ModelAdmin):
    list_display = ("piesa", "comanda", "mecanic", "finalizata", "durata_activa", "timp_standard")
    list_filter = ("mecanic", "finalizata")

import csv
from django.http import HttpResponse
from .models import OperatieLog

@admin.register(OperatieLog)
class OperatieLogAdmin(admin.ModelAdmin):
    list_display = ("piesa", "mecanic", "comanda", "timp_lucrat", "timp_standard", "data_finalizare")
    list_filter = ("mecanic", "data_finalizare")

    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="operatii_log.csv"'

        writer = csv.writer(response)
        writer.writerow(['Piesa', 'Mecanic', 'Comanda', 'Timp Lucrat', 'Timp Standard', 'Data Finalizare'])

        for log in queryset:
            writer.writerow([
                log.piesa,
                log.mecanic.nume,
                f"{log.comanda.client} - {log.comanda.masina}",
                log.timp_lucrat.total_seconds() / 60,  # minute
                log.timp_standard.total_seconds() / 60, # minute
                log.data_finalizare.strftime("%Y-%m-%d %H:%M")
            ])
        return response

    export_csv.short_description = "Export CSV"