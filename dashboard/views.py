from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bitacoras.models import Bitacora
from accounts.models import User

@login_required
def dashboard(request):
    context = {}
    
    user = request.user
    
    if user.user_type == 'apprentice':
        bitacora_count = Bitacora.objects.filter(apprentice=user).count()
        context['bitacora_count'] = bitacora_count
        
        instructors = User.objects.filter(
            instructor_profile__linked_apprentices=user
        )
        context['instructors'] = instructors
        
    elif user.user_type == 'instructor':
        apprentice_count = user.instructor_profile.linked_apprentices.count()
        context['apprentice_count'] = apprentice_count
        
        recent_bitacoras = Bitacora.objects.filter(
            apprentice__in=user.instructor_profile.linked_apprentices.all()
        ).order_by('-upload_date')[:5]
        context['recent_bitacoras'] = recent_bitacoras
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    
    if user.user_type == 'apprentice':
        context['profile'] = user.apprentice_profile
    elif user.user_type == 'instructor':
        context['profile'] = user.instructor_profile
    
    return render(request, 'dashboard/profile.html', context)
