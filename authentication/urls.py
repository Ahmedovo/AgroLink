from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('login_usr',views.login_user,name='login'),
    path('register_usr',views.register,name='register'),
    path('logout_usr',views.logout_user,name='logout_user'),
]
