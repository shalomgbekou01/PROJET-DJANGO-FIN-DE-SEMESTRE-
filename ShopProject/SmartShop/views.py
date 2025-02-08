from django.shortcuts import render, redirect
from .forms import CategorieForm, ProduitForm
from .models import Categorie, Produit, Panier, Client, Achat, Facture
from django.contrib import messages

from django.db.models import Sum
import json


""" CATEGORIE VIEWS """
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




# DASHBOARD
def dashboard_view(request):
    total_categories = Categorie.objects.count()
    total_produits = Produit.objects.count()
    # total_ventes = Vente.objects.count()
    # chiffre_affaires = Vente.objects.aggregate(Sum('total'))['total__sum'] or 0

    # Récupérer les dernières ventes
    # dernieres_ventes = Vente.objects.order_by('-date')[:5]

    # Récupérer les données des ventes pour le graphique
    # ventes_recent = Vente.objects.order_by('date')[:10]
    # dates_ventes = [vente.date.strftime("%d/%m") for vente in ventes_recent]
    # chiffres_ventes = [vente.total for vente in ventes_recent]

    context = {
        'total_categories': total_categories,
        'total_produits': total_produits,
        # 'total_ventes': total_ventes,
        # 'chiffre_affaires': chiffre_affaires,
        # 'dernieres_ventes': dernieres_ventes,
        # 'dates_ventes': json.dumps(dates_ventes),
        # 'chiffres_ventes': json.dumps(chiffres_ventes),
    }
    
    return render(request, 'admin/dashboard.html', context)




# url de la page d'affichage des catégories
# vue liste_categorie

def liste_categorie(request):

    # recupération du name du formulaire
    query = request.GET.get("nom")
    categories = Categorie.objects.all()
    # si une recherche est éffetuée:

    if query:
        categories = Categorie.objects.filter(nomCategorie__icontains = query)
    context = {"categories":categories}
    return render(request, "categories/liste_categorie.html", context)



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

            messages.success(request, "catégorie ajoutée avec succès")
            return redirect("liste_categories")
        else:
            return render(request, "categories/ajout_categorie.html", {"categorieForm":categorieForm})
    else:
        categorieForm = CategorieForm()
    
    return render(request, "categories/ajout_categorie.html", {"categorieForm":categorieForm})


# suppression de catégorie
# supprimer_categorie
def supprimer_categorie(request, cat_id):
    categorie = Categorie.objects.get(id = cat_id)
    categorie.delete()
    messages.success(request, "catégorie supprimée avec succès")
    return redirect( "liste_categories")


# détails catégorie
def details_categorie(request, cat_id):
    categorie = Categorie.objects.get(id = cat_id)
    context = {"categorie":categorie}
    return render(request, "categories/details_categorie.html", context)

# modifier catégorie

def modifier_categorie(request, cat_id):
    categorie = Categorie.objects.get(id=cat_id)

    if request.method == "POST":
        categorieForm = CategorieForm(request.POST, request.FILES)
        if categorieForm.is_valid():
            nom = categorieForm.cleaned_data["nomCategorie"]
            description = categorieForm.cleaned_data["description"]
            image = categorieForm.cleaned_data["imageCategorie"]

            categorie.nomCategorie = nom
            categorie.description = description
            categorie.imageCategorie = image
            categorie.save()

            messages.success(request, "catégorie modifiée avec succès")
            return redirect("liste_categories")
        else:
            return render(request, "categories/modifier_categorie.html", {"categorieForm":categorieForm})
    else:
        categorieForm = CategorieForm(initial={
            "nomCategorie":categorie.nomCategorie,
            "description": categorie.description,
            "imageCategorie":categorie.imageCategorie,
        })
    
    return render(request, "categories/modifier_categorie.html", {"categorieForm":categorieForm})



""" PRODUITS VIEWS """

# ajout produit:
def ajouter_produit(request):
    # si la  méthode de la requête est post:
    if request.method == "POST":
        produitForm = ProduitForm(request.POST, request.FILES)

        if produitForm.is_valid():
            nom = produitForm.cleaned_data["nomProduit"]
            quantite = produitForm.cleaned_data["quantite"]
            prix = produitForm.cleaned_data["prixUnitaire"]
            description = produitForm.cleaned_data["description"]
            image = produitForm.cleaned_data["imageProduit"]
            categorie_id = produitForm.cleaned_data["categorie"]

            categorie = Categorie.objects.get(id = categorie_id)

            produit, created = Produit.objects.get_or_create(
                nomProduit = nom,
                categorie = categorie,
                defaults={
                    'description': description,
                    'prixUnitaire': prix,
                    'imageProduit': image
                }
            )

            if not created:
                produit.quantite += quantite
                produit.save()
            
            else:
                produit.quantite = quantite
                produit.save()

            messages.success(request, "produit ajouté avec succès")
            return redirect("liste_produits")
        else:
            return render(request, "produits/ajout_produit.html", {"produitForm":produitForm})
    else:
        produitForm = ProduitForm()
    
    return render(request, "produits/ajout_produit.html", {"produitForm":produitForm})



# liste des produits
def liste_produits(request):
     # recupération du name du formulaire
    query = request.GET.get("nom")

    # récupération des catégories
    categories = Categorie.objects.all()

    # dictionnaire pour stocker les produits par catégories
    produit_par_categorie  = {}

    for categorie in categories:

        #s'il y a une recherche
        produits = Produit.objects.filter(categorie = categorie)
        if query:
            produits = produits.filter(nomProduit__icontains = query)

        if produits.exists():
            produit_par_categorie[categorie.nomCategorie] = produits

    # si une recherche est éffectuée:

  
    context = {"produits_par_categorie":produit_par_categorie}
    return render(request, "produits/liste_produits.html", context)

# liste des produits d'une catégorie

def categorie_produits(request, categorie_id):
    categorie = Categorie.objects.get(id = categorie_id)
    produits = Produit.objects.filter(categorie = categorie)
    context = {"produits":produits, "categorie" : categorie}
    return render(request, "produits/categorie_produits.html", context)

# détails de produits
def details_produit(request, prod_id):
    produit = Produit.objects.get(id = prod_id)
    context = {"produit":produit}
    return render(request, "produits/details_produit.html", context)


# supprimer un produit
def supprimer_produit(request, prod_id):
    produit = Produit.objects.get(id = prod_id)
    produit.delete()
    messages.success(request, "produit supprimé avec succès")
    return redirect( "liste_produits")


# modifier un produit
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Produit, Categorie
from .forms import ProduitForm

def modifier_produit(request, produit_id):
    # Récupérer le produit ou afficher une erreur 404 s'il n'existe pas
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():

            # Mettre à jour les champs du produit
            produit.nomProduit = form.cleaned_data["nomProduit"]
            produit.categorie = Categorie.objects.get(id=form.cleaned_data["categorie"])
            produit.imageProduit = form.cleaned_data["imageProduit"]
            produit.description = form.cleaned_data["description"]
            produit.quantite = form.cleaned_data["quantite"]
            produit.prixUnitaire = form.cleaned_data["prixUnitaire"]
            
            produit.save()
            messages.success(request, "Le produit a été modifié avec succès !")
            return redirect('details_produit', prod_id=produit.id)  

    else:
        
        donnees_initiales = {
            "nomProduit": produit.nomProduit,
            "categorie": produit.categorie.id,
            "imageProduit": produit.imageProduit,
            "description": produit.description,
            "quantite": produit.quantite,
            "prixUnitaire": produit.prixUnitaire,
        }
        form = ProduitForm(initial=donnees_initiales)

    return render(request, 'produits/modifier_produit.html', {'form': form, 'produit': produit})
