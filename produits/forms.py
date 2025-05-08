# produits/forms.py
from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'saison': forms.Select(attrs={'class': 'form-select'}),
            'cout_revient': forms.NumberInput(attrs={'class': 'form-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'region': forms.TextInput(attrs={'class': 'form-input'}),
        }