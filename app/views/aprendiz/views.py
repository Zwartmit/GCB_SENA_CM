from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from app.models import Aprendiz
from app.forms import AprendizForm

@method_decorator(never_cache, name='dispatch')
def lista_aprendiz(request):
    nombre = {
        'titulo': 'Listado de aprendices',
        'aprendiz': Aprendiz.objects.all()
    }
    return render(request, 'aprendiz/listar.html',nombre)

class PerfilAprendiz(ListView):
    model = Aprendiz
    template_name = 'aprendiz/perfil.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perfil_aprendiz(request):
        aprendiz = {
            'titulo': 'Perfil del aprendiz',
            'aprendiz': Aprendiz.objects.all()
        }
        return render(request, 'aprendiz/perfil.html',aprendiz)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Perfil del aprendiz'
        context['entidad'] = 'Perfil del aprendiz'
        return context
    
###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class AprendizListView(ListView):
    model = Aprendiz
    template_name = 'aprendiz/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de aprendices'
        context['entidad'] = 'Listado de aprendices'
        context['listar_url'] = reverse_lazy('app:aprendiz_lista')
        context['crear_url'] = reverse_lazy('app:aprendiz_crear')
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class AprendizCreateView(CreateView):
    model = Aprendiz
    form_class = AprendizForm
    template_name = 'aprendiz/crear.html'
    success_url = reverse_lazy('app:aprendiz_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar aprendiz'
        context['entidad'] = 'Registrar aprendiz'
        context['error'] = 'Este aprendiz ya está registrado'
        context['listar_url'] = reverse_lazy('app:aprendiz_lista')
        return context
    
    def form_valid(self, form):
        numero_documento = form.cleaned_data.get('numero_documento')

        if Aprendiz.objects.filter(numero_documento=numero_documento).exists():
            form.add_error('numero_documento', 'Ya existe un aprendiz registrado con este número de documento.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        success_url = reverse('app:aprendiz_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class AprendizUpdateView(UpdateView):
    model = Aprendiz
    form_class = AprendizForm
    template_name = 'aprendiz/crear.html'
    success_url = reverse_lazy('app:aprendiz_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar aprendiz'
        context['entidad'] = 'Editar aprendiz'
        context['error'] = 'Este aprendiz ya está registrado'
        context['listar_url'] = reverse_lazy('app:aprendiz_lista')
        return context

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre').lower()
        response = super().form_valid(form)
        success_url = reverse('app:aprendiz_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class AprendizDeleteView(DeleteView):
    model = Aprendiz
    template_name = 'aprendiz/eliminar.html'
    success_url = reverse_lazy('app:aprendiz_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar aprendiz'
        context['entidad'] = 'Eliminar aprendiz'
        context['listar_url'] = reverse_lazy('app:aprendiz_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Aprendiz eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el aprendiz.'})