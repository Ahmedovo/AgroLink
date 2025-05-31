from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from produits.models import Produit
from commandes.models import Commande, LigneCommande
from .models import Cart, CartItem
from agroL.utils import is_client
from authentication.models import User

@login_required
@user_passes_test(is_client)
def product_list(request):
    produits = Produit.objects.all()
    nombre_clients = User.objects.filter(role='ACHETEUR').count()
    nombre_agriculteurs = User.objects.filter(role='AGRI').count()
    nombre_produits = Produit.objects.count()
    return render(request, 'client/product_list.html', {
        'produits': produits,
        'nombre_clients': nombre_clients,
        'nombre_agriculteurs': nombre_agriculteurs,
        'nombre_produits': nombre_produits
    })

@login_required
@user_passes_test(is_client)
def product_search(request):
    query = request.GET.get('q', '')
    produits = Produit.objects.filter(nom__icontains=query) | Produit.objects.filter(categorie__icontains=query)
    return render(request, 'client/product_list.html', {'produits': produits, 'query': query})

@login_required
@user_passes_test(is_client)
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'client/cart.html', {'cart': cart})

@login_required
@user_passes_test(is_client)
def add_to_cart(request, product_id):
    product = get_object_or_404(Produit, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.nom} ajouté au panier !")
    return redirect('client-cart')

@login_required
@user_passes_test(is_client)
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Produit retiré du panier !")
    return redirect('client-cart')

@login_required
@user_passes_test(is_client)
def order_list(request):
    orders = Commande.objects.filter(client=request.user)
    return render(request, 'client/order_list.html', {'orders': orders})

@login_required
@user_passes_test(is_client)
def order_detail(request, order_id):
    order = get_object_or_404(Commande, id=order_id, client=request.user)
    return render(request, 'client/order_detail.html', {'order': order})

@login_required
@user_passes_test(is_client)
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.cartitem_set.exists():
        messages.error(request, "Votre panier est vide !")
        return redirect('client-cart')

    # Create a new order
    order = Commande.objects.create(
        client=request.user,
        idClient=request.user.id,
        statut='RECUE',
        total=0.0
    )

    # Add items to the order
    for item in cart.cartitem_set.all():
        LigneCommande.objects.create(
            commande=order,
            produit=item.product,
            idCommande=order.id,
            idProduit=item.product.id,
            quantite=item.quantity,
            prix_unitaire=item.product.prix_suggere
        )

    # Update order total and clear cart
    order.update_total()
    cart.cartitem_set.all().delete()
    messages.success(request, "Commande passée avec succès !")
    return redirect('client-order-list')