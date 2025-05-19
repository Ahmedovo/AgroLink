from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User, AgentProfile, ClientProfile  # Make sure this matches your actual model names

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
    
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("Raw POST data:", request.POST) 
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            
            # Set additional user attributes if needed
            user.is_active = True  # Activate user immediately
            user.save()  # Now save the user
            
            # Create profile based on role
            role = form.cleaned_data.get('role')
            if role == 'AGRI':
                AgentProfile.objects.create(
                    user=user,
                    nom=form.cleaned_data.get('nom'),
                    region=form.cleaned_data.get('region'),
                    phone=form.cleaned_data.get('phone')
                )
            elif role == 'ACHETEUR':
                ClientProfile.objects.create(
                    user=user,
                    nom=form.cleaned_data.get('nom'),
                    adresse=form.cleaned_data.get('adresse'),
                    company=form.cleaned_data.get('company'),
                    phone=form.cleaned_data.get('phone')
                )
            
            # Log the user in
            login(request, user)
            
            # Success message
            messages.success(request, 'Votre compte a été créé avec succès!')
            
            # Redirect to home or profile page
            return redirect('home')  # Change 'home' to your desired view name
            
        # If form is invalid, errors will be displayed in template
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})
