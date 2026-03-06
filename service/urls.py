# urls.py
from django.urls import path
from .views import login_view, dashboard, logout_view
from .views import start_operatie, pauza_operatie, stop_operatie
from .views import select_mecanic, login_mecanic
from .views import admin_dashboard, creeaza_comanda, creeaza_operatie
from .views import export_raport_csv

urlpatterns = [
    path('', select_mecanic),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('login_mecanic/<int:mecanic_id>/', login_mecanic),
    path('start/<int:operatie_id>/', start_operatie, name='start_operatie'),
    path('pauza/<int:operatie_id>/', pauza_operatie, name='pauza_operatie'),
    path('stop/<int:operatie_id>/', stop_operatie, name='stop_operatie'),
    path('admin_dashboard/', admin_dashboard),
    path('creeaza_comanda/', creeaza_comanda),
    path('creeaza_operatie/', creeaza_operatie),
    path('export_csv/', export_raport_csv, name='export_csv'),
]