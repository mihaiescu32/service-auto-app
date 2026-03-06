from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Mecanicul(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nume = models.CharField(max_length=100)

    def __str__(self):
        return self.nume


class Comanda(models.Model):
    client = models.CharField(max_length=200)
    masina = models.CharField(max_length=200)
    data_creare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.masina}"


class Operatie(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name="operatii")
    piesa = models.CharField(max_length=200)
    mecanic = models.ForeignKey(Mecanicul, on_delete=models.CASCADE)

    start_time = models.DateTimeField(null=True, blank=True)
    timp_total = models.DurationField(default=timedelta)
    timp_standard = models.DurationField(default=timedelta, help_text="Timpul standard în minute")

    este_in_pauza = models.BooleanField(default=False)
    finalizata = models.BooleanField(default=False)

    data_creare = models.DateTimeField(auto_now_add=True)

    data_creare = models.DateTimeField(auto_now_add=True)

    def durata_activa(self):
        total = self.timp_total
        if self.start_time:
            total += timezone.now() - self.start_time
        return round(total.total_seconds() / 60, 2)

    def __str__(self):
        return f"{self.piesa} - {self.mecanic.nume}"
    
class OperatieLog(models.Model):
    operatie = models.ForeignKey(Operatie, on_delete=models.CASCADE)
    mecanic = models.ForeignKey(Mecanicul, on_delete=models.CASCADE)
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    piesa = models.CharField(max_length=200)
    timp_lucrat = models.DurationField()
    timp_standard = models.DurationField()
    data_finalizare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.piesa} - {self.mecanic.nume} - {self.data_finalizare.strftime('%Y-%m-%d')}"