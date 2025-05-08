from django.db import models

from django.db import models
from authentication.models import User
from produits.models import Produit

class Commande(models.Model):
    STATUTS = (
        ('RECUE', 'Reçue'),
        ('PREPARATION', 'En préparation'),
        ('EXPEDIEE', 'Expédiée'),
        ('LIVREE', 'Livrée'),
    )
    idClient = models.IntegerField()
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='RECUE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def update_total(self):
        self.total = sum(
            ligne.prix_unitaire * ligne.quantite 
            for ligne in self.lignecommande_set.all()
        )
        self.save()
    
    def __str__(self):
        return f"Commande #{self.id} - {self.client.email}"

class LigneCommande(models.Model):
    idCommande = models.IntegerField()
    idProduit = models.IntegerField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.commande.update_total()
    
    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"