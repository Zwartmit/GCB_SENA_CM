from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm, ApprenticeRegisterForm, InstructorRegisterForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return redirect('accounts:login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Hola de nuevo, {user.first_name}!")
                return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return render(request, 'accounts/register.html')

def register_apprentice(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = ApprenticeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Cuenta creada con éxito. ¡Hola, {user.first_name}!")
            return redirect('dashboard:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ApprenticeRegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'apprentice'
    })

def register_instructor(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = InstructorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Cuenta creada con éxito. ¡Hola, {user.first_name}!")
            return redirect('dashboard:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InstructorRegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'instructor'
    })
