from django import forms

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

    def valider_nom(self):
        nom = self.cleaned_data.get("nomCategorie")
        if len(nom) < 2:
            raise (forms.ValidationError("le nom de la catégorie doit contenir au moins 2 caractères"))  
        return nom     
    



# classe ProduitForm définissant le  formulaire des produits
class ProduitForm(forms.Form):
    nomProduit = forms.CharField(
        widget= forms.TextInput(attrs= {"class": "input form-control"})
    )
    imageProduit  = forms.ImageField(
        widget= forms.FileInput(attrs= {"class": "input form-control"})
    )
    description = forms.CharField(
        widget= forms.Textarea(attrs= {"class" : "input form-control"})
    )
    quantite = forms.IntegerField(
        widget=forms.NumberInput(attrs= {"class": "input form-control"})
    )
    prixUnitaire = forms.FloatField(
        widget= forms.NumberInput(attrs= {"class": "input form-control"})
    )
    
    


    def valider_nom(self):
        nom = self.cleaned_data.get("nomProduit")
        if len(nom) < 2:
            raise (forms.ValidationError("le nom du produit doit contenir au moins 2 caractères"))  
        return nom     
    
    def valider_quantite(self):
        qte = self.cleaned_data.get("quantite")
        if qte < 0:
            raise (forms.ValidationError("la quantité doit être supérieure à 0"))  
        return qte
    
    def valider_prix(self):
        prix = self.cleaned_data.get("prixUnitaire")
        if prix < 0:
            raise (forms.ValidationError("la prix doit être supérieure à 0"))  
        return prix
    
        