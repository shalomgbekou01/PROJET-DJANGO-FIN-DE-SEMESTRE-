from django.urls import path
from .views import login, dashboard, liste_categorie, ajouter_categorie

urlpatterns = [

    # login: url de la page de connexion
    
    path("", login, name='login'),

    # dashboard: url de la page d'accueil ou tableau de bord
    path("dashboard", dashboard, name='dashboard'),

    # categories: url de la page d'affichage des catégories
    path("categories/liste_categories", liste_categorie, name="liste_categories"),

     # categories: url de la page d'ajout des catégories
    path("categories/ajouter_categorie", ajouter_categorie, name="ajout_categorie")

]
