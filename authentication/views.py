from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Changed from username
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {email}!")
            
            # Redirect based on role
            if user.role == 'AGRI':
                return redirect('agriculteur_dashboard')
            elif user.role == 'ACHETEUR':
                return redirect('acheteur_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    return render(request, 'authentication/login.html')
