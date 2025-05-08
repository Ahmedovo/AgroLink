from django.db import models

# Create your models here.
from django.db import models

class Produit(models.Model):
    CATEGORIES = (
        ('FRUIT', 'Fruits'),
        ('LEGUME', 'Légumes'),
    )
    
    SAISONS = (
        ('PRINTEMPS', 'Printemps'),
        ('ETE', 'Été'), 
        ('AUTOMNE', 'Automne'),
        ('HIVER', 'Hiver'),
    )
    
    # Champs de base
    id_Agent = models.IntegerField()
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=10, choices=CATEGORIES)
    saison = models.CharField(max_length=10, choices=SAISONS)
    cout_revient = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    region = models.CharField(max_length=100)
    prix_suggere = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Méthodes
    def calculer_prix_suggere(self):
        # Placeholder pour la logique ML
        return self.cout_revient * 1.2  # Exemple simple
    
    def save(self, *args, **kwargs):
        if not self.prix_suggere:
            self.prix_suggere = self.calculer_prix_suggere()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} ({self.categorie})"