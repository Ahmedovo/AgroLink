# produits/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit
from .forms import ProduitForm

def product_list(request):
    produits = Produit.objects.all()
    return render(request, 'produits/list.html', {'produits': produits})

def product_create(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProduitForm()
    return render(request, 'produits/form.html', {'form': form})

def product_update(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/form.html', {'form': form})

def product_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('product-list')
    return render(request, 'produits/confirm_delete.html', {'produit': produit})