from django import forms
from .models import Categorie

# classe CategorieForm définissant le  formulaire des catégories
class CategorieForm(forms.Form):
    nomCategorie = forms.CharField(
        label="Nom de la catégorie",
        widget= forms.TextInput(attrs= {"class": "input form-control"})
    )
    imageCategorie  = forms.ImageField(
        label="Image de la ctégorie",
        widget= forms.FileInput(attrs= {"class": "input form-control"})
    )
    description = forms.CharField(
        label="Description de la catégorie",
        widget= forms.Textarea(attrs= {"class" : "input form-control"})
    )

    def clean_nomCategorie(self):
        nom = self.cleaned_data.get("nomCategorie")
        if len(nom) < 2:
            raise (forms.ValidationError("le nom de la catégorie doit contenir au moins 2 caractères"))  
        return nom     
    



# classe ProduitForm définissant le  formulaire des produits
class ProduitForm(forms.Form):
    nomProduit = forms.CharField(
        label= "Nom du produit",
        widget= forms.TextInput(attrs= {"class": "input form-control"})
    )


    categorie = forms.ChoiceField(
        label= "choisissez la categorie",
        choices=[],
        widget= forms.Select(attrs= {"class": "form-select"})
    )


    imageProduit  = forms.ImageField(
        label= "Image du produit",
        widget= forms.FileInput(attrs= {"class": "input form-control"})
    )
    description = forms.CharField(
        label="Description du produit",
        widget= forms.Textarea(attrs= {"class" : "input form-control"})
    )
    quantite = forms.IntegerField(
        label= "Quantité disponible",
        widget=forms.NumberInput(attrs= {"class": "input form-control"})
    )
    prixUnitaire = forms.FloatField(
        label= "Prix unitaire",
        widget= forms.NumberInput(attrs= {"class": "input form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplir le choix des catégories avec les données de la base
        self.fields['categorie'].choices = [(cat.id, cat.nomCategorie) for cat in Categorie.objects.all()]

    
    

    def clean_nomProduit(self):
        nom = self.cleaned_data.get("nomProduit")
        if len(nom) < 2:
            raise (forms.ValidationError("le nom du produit doit contenir au moins 2 caractères"))  
        return nom     
    
    def clean_quantite(self):
        qte = self.cleaned_data.get("quantite")
        if qte < 0:
            raise (forms.ValidationError("la quantité doit être supérieure à 0"))  
        return qte
    
    def clean_prixUnitaire(self):
        prix = self.cleaned_data.get("prixUnitaire")
        if prix < 0:
            raise (forms.ValidationError("le prix doit être supérieur à 0"))  
        return prix
    
        