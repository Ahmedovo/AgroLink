from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('new/', views.product_create, name='product-create'),
    path('<int:pk>/edit/', views.product_update, name='product-update'),
    path('<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('prix-saisonnier/', views.prix_saisonnier, name='prix-saisonnier'),
]