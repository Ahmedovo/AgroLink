from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AgentProfile, ClientProfile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'votre@email.com'})
    )
    role = forms.ChoiceField(
        choices=User.ROLES,
        required=True,
        widget=forms.Select(attrs={'class': 'w-full'})
    )
    nom = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom complet'})
    )
    region = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Votre région'})
    )
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Votre adresse complète', 'rows': 3})
    )
    company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom de votre entreprise'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Votre téléphone'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].required = True

    def clean(self):
            cleaned_data = super().clean()
            role = cleaned_data.get('role')
            
            # Get field values with proper fallbacks
            nom = cleaned_data.get('nom')
            if isinstance(nom, list):  # Handle case where multiple values are submitted
                nom = next((x for x in nom if x.strip()), '').strip()
            else:
                nom = (nom or '').strip()
                
            region = cleaned_data.get('region', '').strip()
            adresse = cleaned_data.get('adresse', '').strip()
            
            print(f"Debug - Role: {role}, Nom: {nom}")  # Debug line
            
            if role == 'AGRI':
                if not nom:
                    self.add_error('nom', 'Ce champ est obligatoire pour les agriculteurs')
                if not region:
                    self.add_error('region', 'Ce champ est obligatoire pour les agriculteurs')
                    
            elif role == 'ACHETEUR':
                if not nom:
                    self.add_error('nom', 'Ce champ est obligatoire pour les acheteurs')
                if not adresse:
                    self.add_error('adresse', 'Ce champ est obligatoire pour les acheteurs')
                    
            # Update cleaned_data with processed values
            cleaned_data['nom'] = nom
            cleaned_data['region'] = region
            cleaned_data['adresse'] = adresse
            
            return cleaned_data