from django.urls import path
from .views import *

urlpatterns = [

    # login: url de la page de connexion
    
    path("", login, name='login'),
    
    # """ CATEGORIE URLS """

    # dashboard: url de la page d'accueil ou tableau de bord
    path("dashboard", dashboard_view, name='dashboard'),

    # categories: url de la page d'affichage des catégories
    path("categories/liste", liste_categorie, name="liste_categories"),

     # categories: url de la page d'ajout des catégories
    path("categories/ajouter", ajouter_categorie, name="ajout_categorie"),

    # supprimer_categorie
    path("categories/supprimer/<int:cat_id>", supprimer_categorie, name="delete_categorie"),

    # détails catégories
    path("categories/détails/<int:cat_id>", details_categorie, name="details_categorie"),

    # modifier categorie
    path("categories/modifier/<int:cat_id>", modifier_categorie, name="modifier_categorie"),


    # """ PRODUIT URL """
    # ajout produit
    path("produits/ajouter", ajouter_produit, name="ajout_produit"),

    # liste des produits
    path("produits/liste", liste_produits, name= "liste_produits"),

    # liste des produits d'une catégorie
    path("produits/categorie_produits/<int:categorie_id>", categorie_produits, name="categorie_produit"),

    # détails produit
    path("produits/details/<int:prod_id>", details_produit, name="details_produit"),

    # supprimer un produit
    path("produits/supprimer/<int:prod_id>", supprimer_produit, name = "delete_produit"),

    # modifier produit

    path("produits/modifier<int:produit_id>", modifier_produit, name= "modifier_produit"),

    # augmenter la quantité d'un produit
    path("produits/add_quantite/<int:p_id>", add_quantite, name = "add_quantite") 

]
