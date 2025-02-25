from django.shortcuts import render, redirect
from .forms import CategorieForm, ProduitForm, ClientForm
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
    total_ventes = Facture.objects.count()
    chiffre_affaires = Facture.objects.aggregate(Sum('prixTotal'))['prixTotal__sum'] or 0

    # Récupérer les dernières ventes
    meilleures_ventes = Facture.objects.order_by('-prixTotal')[:3]

    # Récupérer les données des ventes pour le graphique
    ventes_recent = Facture.objects.order_by('dateFacture')
    dates_ventes = [vente.dateFacture.strftime("%d/%m") for vente in ventes_recent]
    chiffres_ventes = [vente.prixTotal for vente in ventes_recent]

    # les produits en faible stock
    produits_faible_stock = Produit.objects.filter(quantite__lt=5)

    # produits les plus vendus
    plus_vendus = Achat.objects.order_by("-quantite")[:3]

    context = {
        'total_categories': total_categories,
        'total_produits': total_produits,
        'total_ventes': total_ventes,
        'chiffre_affaires': chiffre_affaires,
        'meilleures_ventes':meilleures_ventes,
        'dates_ventes': json.dumps(dates_ventes),
        'chiffres_ventes': json.dumps(chiffres_ventes),
        'produits_faible_stock': produits_faible_stock,
        'plus_vendus':plus_vendus
    }
    return render(request, 'admin/dashboard.html', context)




# url de la page d'affichage des catégories'
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

            oCategorie1 = Categorie(nomCategorie= nom, description= description, imageCategorie= image)
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
    nbreproduits = Produit.objects.filter(categorie = categorie).count()
    categorie.nbreProduit = nbreproduits
    categorie.save()
    context = {"categorie":categorie}
    
    return render(request, "categories/details_categorie.html", context)

# modifier catégorie

def modifier_categorie(request, cat_id):
    categorie = Categorie.objects.get(id=cat_id)
    nbreproduits = Produit.objects.filter(categorie = categorie).count()

    if request.method == "POST":
        categorieForm = CategorieForm(request.POST, request.FILES)
        if categorieForm.is_valid():
            nom = categorieForm.cleaned_data["nomCategorie"]
            description = categorieForm.cleaned_data["description"]
            image = categorieForm.cleaned_data["imageCategorie"]

            categorie.nomCategorie = nom
            categorie.description = description
            categorie.imageCategorie = image
            categorie.nbreProduit = nbreproduits
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

            categorie = Categorie.objects.get(produit = produit)
            categorie.nbreProduit += 1
            categorie.save()


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
    categories = Categorie.objects.all()
     # recupération du name du formulaire
    if request.method == "POST":
        categorie_name = request.POST.get("categorie")
        nom = request.POST.get('nom')
        if categorie_name:
            categorie = Categorie.objects.filter(nomCategorie__icontains = categorie_name)
            produits = Produit.objects.filter(categorie__in = categorie).order_by("nomProduit")
        else:
            produits = Produit.objects.filter(nomProduit__icontains = nom).order_by("id")
    else:
        produits = Produit.objects.all().order_by("nomProduit")
  
    context = {"produits":produits, "categories":categories}
    return render(request, "produits/liste_produits.html", context)

# liste des produits d'une catégorie

def categorie_produits(request, categorie_id):
    categorie = Categorie.objects.get(id = categorie_id)
    produits = Produit.objects.filter(categorie = categorie)

    if request.method =="POST":
        nom = request.POST.get("nom")
        produits = produits.filter(nomProduit__icontains = nom)
        
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

# augmenter quantité d'un produit

def add_quantite(request, p_id):
    # récupérer le produit à modifier
    produit = Produit.objects.get(id = p_id)

    # récupérer la quantité saisie
    quantite = request.POST.get("quantite")

    if (int)(quantite) < 0:
        messages.error(request, "la quantité doit être supérieure à 0", extra_tags="danger")
        return redirect("details_produit", prod_id=p_id)
        
    # incrémenter la quantité
    produit.quantite += int(quantite)

    messages.success(request, "quantité du produit augmenté avec succès")

    # mettre à jour
    produit.save()

    return redirect("details_produit", prod_id=p_id)



# ------------------------ PANIERS ACHATS VENTES FACTURES ---------------------------------
    
#  effectuer une vente -> enrégistrer le client -> créer un panier
def methode_achat(request):
    return render(request, "achats/methode_achat.html")

# ajouter un client
def ajouter_client_clic(request):

    oClient = Client(nomClient = "", prenomClient = "", adresseClient =  "", telephone ="")
    oClient.save()

    # créer un panier pour le client
    oPanier1 = Panier(client = oClient)
    oPanier1.save()
    
    messages.success(request, "panier créé avec succès")
    return redirect("liste_produits")

    
# recupérer les infos du client
def ajouter_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)

        # validation

        if form.is_valid():
            nom = form.cleaned_data["nomClient"]
            prenom = form.cleaned_data["prenomClient"]
            adresse = form.cleaned_data["adresseClient"]
            tel = form.cleaned_data["telephone"]

            # enrégistrer le client
            oClient1 = Client(nomClient = nom, prenomClient = prenom, adresseClient =  adresse, telephone = tel)
            oClient1.save()

            # créer un panier pour le client
            oPanier1 = Panier(client = oClient1)
            oPanier1.save()
            messages.success(request, "panier créé avec succès")
            return redirect("liste_produits")
    else:
        form = ClientForm()
        return render(request, "achats/ajout_panier.html", {"form":form})

# selectionner un produit

def selectionner(request, prod_id):
    produit = Produit.objects.get(id = prod_id)
    paniers = Panier.objects.filter(statut = "en cours").order_by("-id")
    return render(request, "achats/selectionner.html", {"produit":produit, "paniers":paniers})


# ajout des produits au panier

def ajouter_au_panier(request, prod_id):
    if request.method == "POST":
        panier_id = request.POST.get("panier")

        produit = Produit.objects.get(id = prod_id)
        panier = Panier.objects.get(id = panier_id)
        quantite = int(request.POST.get("quantite",1))

        # vérifier si la quantité est suffisante
        if quantite > produit.quantite:
            messages.error(request, "Stock insuffisant.", extra_tags="danger")
            return redirect("selectionner", prod_id = prod_id)

                

        # Ajouter le produit au panier

        achats = Achat.objects.filter(panier = panier)
                
        # vérifier si le produit est déjà ajouté au panier
        if achats:
            for achat in achats:
                if achat.produit == produit:
                    achat.quantite += quantite
                    achat.prixAchat = achat.quantite * produit.prixUnitaire
                    achat.save()
        
                    messages.success(request, "Produit ajouté au panier avec succès !")
                    return redirect("liste_produits")
                
        
        prix_total_achat = quantite * produit.prixUnitaire
        achat = Achat(produit=produit, panier=panier, quantite=quantite, prixAchat=prix_total_achat)
        achat.save()

        # Mettre à jour le prix total du panier
        panier.prixTotal += prix_total_achat
        panier.nbreProduit += quantite
        panier.save()


        messages.success(request, "Produit ajouté au panier avec succès !")
        return redirect("liste_produits")

    # return render(request, "achats/ajouter_au_panier.html", {"produit": produit})


# Vue pour afficher le panier
def consulter_panier(request, panier_id):
    panier = Panier.objects.get(id = panier_id)
    achats = Achat.objects.filter(panier=panier)
    total = sum(achat.prixAchat for achat in achats)

    return render(request, "achats/panier.html", {"achats": achats, "total": total, "panier":panier})

# liste des paniers

def liste_panier(request):
    paniers = Panier.objects.all().order_by("-id")
    return render(request, "achats/liste_panier.html", {"paniers":paniers})

# supprimer le panier
def supprimer_panier(request, panier_id):
    panier = Panier.objects.get(id = panier_id)
    panier.delete()
    messages.success(request, "panier supprimé avec succès")
    return redirect("liste_panier")

# vider un panier

def vider_panier(request, panier_id):
    panier = Panier.objects.get(id = panier_id)
    achats = Achat.objects.filter(panier = panier)

    achats.delete()
    messages.success(request, "panier vidé avec succès")
    return redirect("panier", panier_id = panier_id)

# valider achat

def valider_panier(request, panier_id):
    panier = Panier.objects.get(id = panier_id)
    achats = Achat.objects.filter(panier = panier)
    
    for achat in achats:
        achat.produit.quantite -= achat.quantite
        achat.produit.save()

    panier.statut = "validé"
    panier.save()
    


    # créer une facture pour le client
    dernier_numero = Facture.objects.count()
    num_facture = f"{dernier_numero + 1:04d}"
    
    oFacture1 = Facture(numeroFacture = num_facture, client = panier.client, prixTotal = panier.prixTotal, panier = panier)            
    oFacture1.save()

    messages.success(request, "panier validé avec succès")
    return redirect("facture", panier_id = panier_id)

# liste des achats
def liste_achats(request):

    if request.method =="POST":
        date_achat = request.POST.get("date")
        achats = Achat.objects.filter(dateAchat = date_achat, panier__statut = "validé")

    achats = Achat.objects.filter(panier__statut = "validé").order_by("dateAchat")

    return render(request, "achats/liste_achats.html", {"achats":achats})
# supprimer un achat du panier

def supprimer_achat(request, id_achat, id_panier):
    achat = Achat.objects.get(id = id_achat)
    panier = Panier.objects.get(id = id_panier)
    panier.nbreProduit -= achat.quantite
    panier.save()
    achat.delete()
    
    messages.success(request,"produit retiré du panier")
    return redirect("panier", panier_id = id_panier)



# facture

def facture(request, panier_id):
    panier = Panier.objects.get(id = panier_id)
    facture = Facture.objects.get(client = panier.client)

    achats = Achat.objects.filter(panier=panier)

    context = {
        "achats": achats,
        "facture":facture
    }
    return render(request, "achats/facture.html", context = context)