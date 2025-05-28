from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, StdDev
from django.conf import settings
from decimal import Decimal  # Ajout important

class Produit(models.Model):
    CATEGORIES = (
        ('FRUIT', 'Fruits'),
        ('LEGUME', 'Légumes'),
        ('CEREALE', 'Céréales'),
        ('VIANDE', 'Viande'),
        ('LAITIER', 'Produits laitiers'),
    )
    
    SAISONS = (
        ('PRINTEMPS', 'Printemps'),
        ('ETE', 'Été'), 
        ('AUTOMNE', 'Automne'),
        ('HIVER', 'Hiver'),
    )
    
    # Champs de base
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='produits'
    )
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=10, choices=CATEGORIES)
    saison = models.CharField(max_length=10, choices=SAISONS)
    cout_revient = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    region = models.CharField(max_length=100)
    prix_suggere = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_min_saisonnier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_max_saisonnier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Méthodes
    def calculer_prix_suggere(self):
        # Utiliser Decimal pour la constante
        return self.cout_revient * Decimal('1.2')
    
    def calculer_plage_prix_saisonnier(self):
        """Calcule la plage de prix recommandée basée sur les prix historiques de tous les agents"""
        # Récupère les produits similaires de tous les agents
        produits_similaires = Produit.objects.filter(
            nom=self.nom,
            saison=self.saison
        ).exclude(pk=self.pk)
        
        if produits_similaires.exists():
            # Calcule la moyenne et l'écart type pour tous les agents
            stats = produits_similaires.aggregate(
                avg=Avg('prix_suggere'),
                stddev=StdDev('prix_suggere')
            )
            
            if stats['avg'] is not None and stats['stddev'] is not None:
                # Convertir les float en Decimal
                avg = Decimal(str(stats['avg']))
                stddev = Decimal(str(stats['stddev']))
                
                min_val = max(avg - stddev, self.cout_revient * Decimal('1.1'))
                max_val = min(avg + stddev, self.cout_revient * Decimal('1.5'))
                return min_val, max_val
        
        # Valeurs par défaut avec Decimal
        min_default = self.cout_revient * Decimal('1.15')
        max_default = self.cout_revient * Decimal('1.25')
        return min_default, max_default
    
    def save(self, *args, **kwargs):
        # Calcul du prix suggéré
        if not self.prix_suggere:
            self.prix_suggere = self.calculer_prix_suggere()
        
        # Calcul de la plage saisonnière (basée sur tous les agents)
        min_val, max_val = self.calculer_plage_prix_saisonnier()
        self.prix_min_saisonnier = min_val
        self.prix_max_saisonnier = max_val
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} ({self.categorie})"