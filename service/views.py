from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Operatie, Mecanicul


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Date invalide"})

    return render(request, "login.html")


@login_required
def dashboard(request):
    mecanic = Mecanicul.objects.get(user=request.user)
    operatii = Operatie.objects.filter(mecanic=mecanic, finalizata=False)

    return render(request, "service/operatii_mecanic.html", {
        "mecanic": mecanic,
        "operatii": operatii
    })


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def start_operatie(request, operatie_id):
    operatie = get_object_or_404(Operatie, id=operatie_id)

    if operatie.mecanic.user == request.user and not operatie.finalizata:
        operatie.start_time = timezone.now()
        operatie.este_in_pauza = False
        operatie.save()

    return redirect("dashboard")


@login_required
def pauza_operatie(request, operatie_id):
    operatie = get_object_or_404(Operatie, id=operatie_id)

    if operatie.mecanic.user == request.user and operatie.start_time:
        durata = timezone.now() - operatie.start_time
        operatie.timp_total += durata
        operatie.start_time = None
        operatie.este_in_pauza = True
        operatie.save()

    return redirect("dashboard")


@login_required
def stop_operatie(request, operatie_id):
    operatie = get_object_or_404(Operatie, id=operatie_id)

    if operatie.mecanic.user == request.user:
        if operatie.start_time:
            durata = timezone.now() - operatie.start_time
            operatie.timp_total += durata

        operatie.start_time = None
        operatie.finalizata = True
        operatie.este_in_pauza = False
        operatie.save()

    return redirect("dashboard")

from django.contrib.auth.models import User


def select_mecanic(request):

    mecanici = Mecanicul.objects.all()

    return render(request,"select_mecanic.html",{
        "mecanici": mecanici
    })


def login_mecanic(request, mecanic_id):

    mecanic = Mecanicul.objects.get(id=mecanic_id)

    user = mecanic.user

    login(request,user)

    return redirect("dashboard")

from .models import Comanda


@login_required
def admin_dashboard(request):

    mecanici = Mecanicul.objects.all()

    comenzi = Comanda.objects.all()

    operatii = Operatie.objects.filter(finalizata=False)

    return render(request,"admin_dashboard.html",{

        "mecanici": mecanici,
        "comenzi": comenzi,
        "operatii": operatii

    })

@login_required
def creeaza_comanda(request):

    if request.method == "POST":

        client = request.POST.get("client")

        masina = request.POST.get("masina")

        Comanda.objects.create(

            client=client,
            masina=masina

        )

    return redirect("/admin_dashboard/")

@login_required
def creeaza_operatie(request):
    if request.method == "POST":
        comanda_id = request.POST.get("comanda")
        piesa = request.POST.get("piesa")
        mecanic_id = request.POST.get("mecanic")
        timp_standard_minute = request.POST.get("timp_standard") or 0  # poate fi 0 dacă nu e completat
        timp_standard = timedelta(minutes=int(timp_standard_minute))

        comanda = Comanda.objects.get(id=comanda_id)
        mecanic = Mecanicul.objects.get(id=mecanic_id)

        # Creare operatie o singură dată
        Operatie.objects.create(
            comanda=comanda,
            piesa=piesa,
            mecanic=mecanic,
            timp_standard=timp_standard
        )

    return redirect("/admin_dashboard/")
from .models import OperatieLog

@login_required
def stop_operatie(request, operatie_id):
    operatie = get_object_or_404(Operatie, id=operatie_id)

    if operatie.mecanic.user == request.user:
        if operatie.start_time:
            durata = timezone.now() - operatie.start_time
            operatie.timp_total += durata

        operatie.start_time = None
        operatie.finalizata = True
        operatie.este_in_pauza = False
        operatie.save()

        # Salvăm log-ul pentru export
        OperatieLog.objects.create(
            operatie=operatie,
            mecanic=operatie.mecanic,
            comanda=operatie.comanda,
            piesa=operatie.piesa,
            timp_lucrat=operatie.timp_total,
            timp_standard=operatie.timp_standard
        )

    return redirect("dashboard")

import csv
from django.http import HttpResponse
from .models import Operatie

@login_required
def export_raport_csv(request):
    # doar pentru admin
    if not request.user.is_staff:
        return HttpResponse("Nu ai acces", status=403)

    # pregătim CSV-ul
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_operatii.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID Operatie', 'Comanda', 'Piesa', 'Mecanic', 'Timp lucrat', 'Timp standard', 'Finalizata'])

    operatii = Operatie.objects.all()
    for op in operatii:
        writer.writerow([
            op.id,
            f"{op.comanda.client} - {op.comanda.masina}",
            op.piesa,
            op.mecanic.nume,
            round(op.durata_activa(), 2),
            round(op.timp_standard.total_seconds() / 60, 2),
            op.finalizata
        ])

    return response