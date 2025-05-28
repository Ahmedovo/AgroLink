from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom', 'categorie', 'saison', 'cout_revient', 
            'stock', 'region', 'image', 'prix_suggere'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'saison': forms.Select(attrs={'class': 'form-select'}),
            'cout_revient': forms.NumberInput(attrs={'class': 'form-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'region': forms.TextInput(attrs={'class': 'form-input'}),
            'prix_suggere': forms.NumberInput(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'prix_suggere': 'Prix suggéré (DH/kg)'
        }
        help_texts = {
            'prix_suggere': 'Le prix que vous souhaitez fixer'
        }