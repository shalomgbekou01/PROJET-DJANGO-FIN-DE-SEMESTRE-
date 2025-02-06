from django.shortcuts import render, redirect
from .forms import CategorieForm, ProduitForm
from .models import Categorie, Produit, Panier, Client, Achat, Facture



# url de la page de connexion
# login view

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
    # logique pour vérifier si les identifiants correspondes à ceux exigés
        if((username ==  "admin") and (password == "admin01")):
            return redirect("dashboard")
        else:
            error = "nom d'utilisateur ou mot de passe incorrecte"
            return render(request, "admin/login.html", {"erreur" : error})

    return render(request, 'admin/login.html')

# url de la page de déconnexion
# logout view

def logout(request):
    return redirect("login")

# url de la page d'acueil
# vue dashboard

def dashboard(request):
    return render(request, 'admin/dashboard.html')



# url de la page d'affichage des catégories
# vue liste_categorie

def liste_categorie(request):
    return render(request, "categories/liste_categorie.html")



# url de la page d'ajout de catégorie
# vue ajouter_categorie

def ajouter_categorie(request):
    # si la  méthode de la requête est post:
    if request.method == "POST":
        categorieForm = CategorieForm(request.POST, request.FILES)
        if categorieForm.is_valid():
            nom = categorieForm.cleaned_data["nomCategorie"]
            description = categorieForm.cleaned_data["description"]
            image = categorieForm.cleaned_data["imageCategorie"]

            oCategorie1 = Categorie(nomCategorie= nom, description= description, imageCategorie= image )
            oCategorie1.save()

            return redirect("liste_categories")
        else:
            return render(request, "categories/ajout_categorie.html", {"categorieForm":categorieForm})
    else:
        categorieForm = CategorieForm()
    
    return render(request, "categories/ajout_categorie.html", {"categorieForm":categorieForm})

