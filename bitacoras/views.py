from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Bitacora
from .forms import BitacoraUploadForm, LinkApprenticeForm
from accounts.models import User

def user_is_apprentice(user):
    return user.user_type == 'apprentice'

def user_is_instructor(user):
    return user.user_type == 'instructor'

@login_required
def list_bitacoras(request):
    if not user_is_apprentice(request.user):
        messages.error(request, "Solo los aprendices pueden acceder a esta página.")
        return redirect('dashboard:dashboard')
    
    bitacoras = Bitacora.objects.filter(apprentice=request.user)
    return render(request, 'bitacoras/list_bitacoras.html', {'bitacoras': bitacoras})

@login_required
def upload_bitacora(request):
    if not user_is_apprentice(request.user):
        messages.error(request, "Solo los aprendices pueden subir bitácoras.")
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = BitacoraUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bitacora = form.save(commit=False)
            bitacora.apprentice = request.user
            bitacora.filename = request.FILES['file'].name
            bitacora.save()
            messages.success(request, "¡Bitácora subida exitosamente!")
            return redirect('bitacoras:list_bitacoras')
    else:
        form = BitacoraUploadForm()
    
    return render(request, 'bitacoras/upload_bitacora.html', {'form': form})

@login_required
def delete_bitacora(request, pk):
    bitacora = get_object_or_404(Bitacora, pk=pk)
    
    if bitacora.apprentice != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta bitácora.")
    
    if request.method == 'POST':
        bitacora.delete()
        messages.success(request, "¡Bitácora eliminada exitosamente!")
        return redirect('bitacoras:list_bitacoras')
    
    return render(request, 'bitacoras/confirm_delete.html', {'bitacora': bitacora})

@login_required
def apprentice_list(request):
    if not user_is_instructor(request.user):
        messages.error(request, "Solo los instructores pueden acceder a esta página.")
        return redirect('dashboard:dashboard')
    
    linked_apprentices = request.user.instructor_profile.linked_apprentices.all()
    return render(request, 'bitacoras/apprentice_list.html', {'apprentices': linked_apprentices})

@login_required
def apprentice_bitacoras(request, apprentice_id):
    if not user_is_instructor(request.user):
        messages.error(request, "Solo los instructores pueden acceder a esta página.")
        return redirect('dashboard:dashboard')
    
    apprentice = get_object_or_404(User, pk=apprentice_id, user_type='apprentice')
    
    if apprentice not in request.user.instructor_profile.linked_apprentices.all():
        return HttpResponseForbidden("No tienes permiso para ver las bitácoras de este aprendiz.")
    
    bitacoras = Bitacora.objects.filter(apprentice=apprentice)
    return render(request, 'bitacoras/apprentice_bitacoras.html', {
        'apprentice': apprentice,
        'bitacoras': bitacoras
    })

@login_required
def link_apprentice(request):
    if not user_is_instructor(request.user):
        messages.error(request, "Solo los instructores pueden vincular aprendices.")
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = LinkApprenticeForm(request.POST, instructor=request.user)
        if form.is_valid():
            apprentice = form.cleaned_data['apprentice']
            request.user.instructor_profile.linked_apprentices.add(apprentice)
            messages.success(request, f"¡Aprendiz {apprentice.get_full_name()} vinculado exitosamente!")
            return redirect('bitacoras:apprentice_list')
    else:
        form = LinkApprenticeForm(instructor=request.user)
    
    return render(request, 'bitacoras/link_apprentice.html', {'form': form})

@login_required
def unlink_apprentice(request, apprentice_id):
    if not user_is_instructor(request.user):
        messages.error(request, "Solo los instructores pueden desvincular aprendices.")
        return redirect('dashboard:dashboard')
    
    apprentice = get_object_or_404(User, pk=apprentice_id, user_type='apprentice')
    
    if request.method == 'POST':
        request.user.instructor_profile.linked_apprentices.remove(apprentice)
        messages.success(request, f"¡Aprendiz {apprentice.get_full_name()} desvinculado exitosamente!")
        return redirect('bitacoras:apprentice_list')
    
    return render(request, 'bitacoras/confirm_unlink.html', {'apprentice': apprentice})
