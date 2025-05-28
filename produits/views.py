from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit
from .forms import ProduitForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, StdDev

@login_required
def product_list(request):
    produits = Produit.objects.filter(agent=request.user)
    return render(request, 'produits/list.html', {'produits': produits})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.agent = request.user
            produit.save()
            return redirect('product-list')
    else:
        form = ProduitForm()
    
    return render(request, 'produits/form.html', {'form': form})

@login_required
def product_update(request, pk):
    produit = get_object_or_404(Produit, pk=pk, agent=request.user)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProduitForm(instance=produit)
    
    return render(request, 'produits/form.html', {'form': form, 'produit': produit})

@login_required
def product_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk, agent=request.user)
    
    if request.method == 'POST':
        produit.delete()
        return redirect('product-list')
    
    return render(request, 'produits/confirm_delete.html', {'produit': produit})

@login_required
def prix_saisonnier(request):
    nom = request.GET.get('nom')
    saison = request.GET.get('saison')
    
    # Récupère les produits similaires de tous les agents
    produits_similaires = Produit.objects.filter(
        nom=nom,
        saison=saison
    )
    
    if produits_similaires.exists():
        # Calcule les statistiques globales
        stats = produits_similaires.aggregate(
            avg=Avg('prix_suggere'),
            stddev=StdDev('prix_suggere')
        )
        
        if stats['avg'] is not None and stats['stddev'] is not None:
            min_val = max(stats['avg'] - stats['stddev'], 0)
            max_val = stats['avg'] + stats['stddev']
            
            return JsonResponse({
                'min': round(min_val, 2),
                'max': round(max_val, 2),
                'count': produits_similaires.count()
            })
    
    # Valeurs par défaut si pas d'historique
    return JsonResponse({
        'min': None,
        'max': None,
        'message': 'Aucune donnée historique pour cette combinaison'
    })