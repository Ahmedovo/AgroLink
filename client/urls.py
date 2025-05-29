from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='client-product-list'),
    path('products/search/', views.product_search, name='client-product-search'),
    path('cart/', views.cart_view, name='client-cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='client-add-to-cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='client-remove-from-cart'),
    path('orders/', views.order_list, name='client-order-list'),
    path('orders/<int:order_id>/', views.order_detail, name='client-order-detail'),
    path('checkout/', views.checkout, name='client-checkout'),
]