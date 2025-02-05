from django.urls import path
from .views import login, dashboard

urlpatterns = [

    # login: url de la page de connexion
    path("", login, name='login'),

    # dashboard: url redirrigeant vers la page d'accueil ou tableau de bord
    path("dashboard", dashboard, name='dashboard'),
]
