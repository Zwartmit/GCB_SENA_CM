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
    """List bitacoras for the current apprentice"""
    if not user_is_apprentice(request.user):
        messages.error(request, "Only apprentices can access this page.")
        return redirect('dashboard:dashboard')
    
    bitacoras = Bitacora.objects.filter(apprentice=request.user)
    return render(request, 'bitacoras/list_bitacoras.html', {'bitacoras': bitacoras})

@login_required
def upload_bitacora(request):
    """Upload a new bitacora"""
    if not user_is_apprentice(request.user):
        messages.error(request, "Only apprentices can upload bitácoras.")
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = BitacoraUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bitacora = form.save(commit=False)
            bitacora.apprentice = request.user
            bitacora.filename = request.FILES['file'].name
            bitacora.save()
            messages.success(request, "Bitácora uploaded successfully!")
            return redirect('bitacoras:list_bitacoras')
    else:
        form = BitacoraUploadForm()
    
    return render(request, 'bitacoras/upload_bitacora.html', {'form': form})

@login_required
def delete_bitacora(request, pk):
    """Delete a bitacora"""
    bitacora = get_object_or_404(Bitacora, pk=pk)
    
    # Security check: only allow the owner to delete
    if bitacora.apprentice != request.user:
        return HttpResponseForbidden("You don't have permission to delete this bitácora.")
    
    if request.method == 'POST':
        bitacora.delete()
        messages.success(request, "Bitácora deleted successfully!")
        return redirect('bitacoras:list_bitacoras')
    
    return render(request, 'bitacoras/confirm_delete.html', {'bitacora': bitacora})

@login_required
def apprentice_list(request):
    """List all apprentices linked to the current instructor"""
    if not user_is_instructor(request.user):
        messages.error(request, "Only instructors can access this page.")
        return redirect('dashboard:dashboard')
    
    linked_apprentices = request.user.instructor_profile.linked_apprentices.all()
    return render(request, 'bitacoras/apprentice_list.html', {'apprentices': linked_apprentices})

@login_required
def apprentice_bitacoras(request, apprentice_id):
    """View bitacoras for a specific apprentice"""
    if not user_is_instructor(request.user):
        messages.error(request, "Only instructors can access this page.")
        return redirect('dashboard:dashboard')
    
    apprentice = get_object_or_404(User, pk=apprentice_id, user_type='apprentice')
    
    # Security check: only allow instructors linked to this apprentice
    if apprentice not in request.user.instructor_profile.linked_apprentices.all():
        return HttpResponseForbidden("You don't have permission to view this apprentice's bitácoras.")
    
    bitacoras = Bitacora.objects.filter(apprentice=apprentice)
    return render(request, 'bitacoras/apprentice_bitacoras.html', {
        'apprentice': apprentice,
        'bitacoras': bitacoras
    })

@login_required
def link_apprentice(request):
    """Link an apprentice to the current instructor"""
    if not user_is_instructor(request.user):
        messages.error(request, "Only instructors can link apprentices.")
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = LinkApprenticeForm(request.POST, instructor=request.user)
        if form.is_valid():
            apprentice = form.cleaned_data['apprentice']
            request.user.instructor_profile.linked_apprentices.add(apprentice)
            messages.success(request, f"Apprentice {apprentice.get_full_name()} linked successfully!")
            return redirect('bitacoras:apprentice_list')
    else:
        form = LinkApprenticeForm(instructor=request.user)
    
    return render(request, 'bitacoras/link_apprentice.html', {'form': form})

@login_required
def unlink_apprentice(request, apprentice_id):
    """Unlink an apprentice from the current instructor"""
    if not user_is_instructor(request.user):
        messages.error(request, "Only instructors can unlink apprentices.")
        return redirect('dashboard:dashboard')
    
    apprentice = get_object_or_404(User, pk=apprentice_id, user_type='apprentice')
    
    if request.method == 'POST':
        request.user.instructor_profile.linked_apprentices.remove(apprentice)
        messages.success(request, f"Apprentice {apprentice.get_full_name()} unlinked successfully!")
        return redirect('bitacoras:apprentice_list')
    
    return render(request, 'bitacoras/confirm_unlink.html', {'apprentice': apprentice})
