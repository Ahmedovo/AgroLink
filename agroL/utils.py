# utils.py or in your views file
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'  # Assuming `role` is a field on your User model

def is_agri(user):
    return user.is_authenticated and user.role == 'AGRI'

def is_client(user):
    return user.is_authenticated and user.role == 'ACHETEUR'