from django.db import models

# Classe Client définissant un client
class Client(models.Model):
    nomClient = models.CharField(max_length=255)
    prenomClient = models.CharField(max_length=255)
    adresseClient = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nomClient} {self.prenomClient}"


# Classe Categorie définissant la catégorie d'un produit
class Categorie(models.Model):
    nomCategorie = models.CharField(max_length=255)
    dateAjout = models.DateTimeField(auto_now=True)
    imageCategorie = models.ImageField(upload_to='categories/', null=False, default="default.png")
    description = models.TextField(default="description categorie")
    nbreProduit = models.IntegerField(default=0)

    def __str__(self):
        return self.nomCategorie


# Classe Produit définissant un produit
class Produit(models.Model):
    nomProduit = models.CharField(max_length=255)
    imageProduit = models.ImageField(upload_to='produits/')
    description = models.TextField()
    quantite = models.IntegerField(default=0)
    prixUnitaire = models.FloatField(default=0.0)
    dateAjout = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomProduit


# Classe Facture définissant la facture d'un client
class Facture(models.Model):
    numeroFacture = models.CharField(max_length=50, unique=True)
    prixTotal = models.FloatField(default=0.0)
    dateFacture = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Facture {self.numeroFacture}"


# Classe Panier définissant le panier d'un client
class Panier(models.Model):
    nbreProduit = models.IntegerField(default=0)
    prixTotal = models.FloatField(default=0.0)
    statut = models.CharField(
        choices=[("en cours", "En Cours"), ("validé", "Validé")],
        max_length=10,
        default="en cours"
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Panier de {self.client.nomClient}"


# Classe Achat définissant un achat effectué par le client
class Achat(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)  # Un produit peut être acheté plusieurs fois
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)    # Un panier contient plusieurs achats
    facture = models.ForeignKey(Facture, on_delete=models.SET_NULL, null=True, blank=True)  # Peut être null avant facturation
    prixAchat = models.FloatField(default=0.0)
    quantite = models.IntegerField(default=1)
    dateAchat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nomProduit} - {self.prixAchat} FCFA"
