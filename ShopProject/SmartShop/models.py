from django.db import models

# classe Client définissant un client
class Client(models.Model):
    nomClient = models.CharField(max_length=255)
    prenomClient = models.CharField(max_length=255)
    prenomClient = models.CharField(max_length=255)
    adresseClient = models.CharField(max_length=255)

    def __str__(self):
        return f" {self.nomClient} {self.prenomClient}"


# classe Categorie définissant la catégorie d'un produit
class Categorie(models.Model):
    nomCategorie = models.CharField(max_length=255)
    dateAjout = models.DateField(auto_now=True)
    imageCategorie = models.ImageField(upload_to='categories/', null=False, default="default.png")
    description = models.TextField(default="description categorie")

    def __str__(self):
        return f" {self.nom_categorie}"



# classe Produit définissant un produit
class Produit(models.Model):
    nomProduit = models.CharField(max_length=255)
    imageProduit  = models.ImageField(null=False, upload_to='produits/')
    description = models.TextField()
    quantite = models.IntegerField(default=0)
    prixUnitaire = models.FloatField(default=0.0)
    dateAjout = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.nomProduit}"



# classe Facture définissant la facture d'un client
class Facture(models.Model):
    numeroFacture = models.CharField(max_length=50)
    prixTotal = models.FloatField(default=0.0)
    dateFacture = models.DateTimeField(auto_now=True)



# classe Panier définissant le panier d'un client
class Panier(models.Model):
    nbreProduit = models.IntegerField(default=0)
    prixTotal = models.FloatField(default=0.0)
    statut = models.CharField(
        choices=[("en cours", "En Cours"), ("validé", "Validé")],
        default="en cours"
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE)



# classe Achat définissant un achat éffectué par le client
class Achat(models.Model):
    prixAchat = models.FloatField(default=0.0)
    dateAchat = models.DateTimeField(auto_now=True)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)