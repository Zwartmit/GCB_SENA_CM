from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from app.models import Instructor
from app.forms import InstructorForm

@method_decorator(never_cache, name='dispatch')
def lista_instructor(request):
    nombre = {
        'titulo': 'Listado de instructores',
        'instructor': Instructor.objects.all()
    }
    return render(request, 'instructor/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class InstructorListView(ListView):
    model = Instructor
    template_name = 'instructor/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de instructores'
        context['entidad'] = 'Listado de instructores'
        context['listar_url'] = reverse_lazy('app:instructor_lista')
        context['crear_url'] = reverse_lazy('app:instructor_crear')
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class InstructorCreateView(CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'instructor/crear.html'
    success_url = reverse_lazy('app:instructor_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar instructor'
        context['entidad'] = 'Registrar instructor'
        context['error'] = 'Este instructor ya está registrado'
        context['listar_url'] = reverse_lazy('app:instructor_lista')
        return context
    
    def form_valid(self, form):
        numero_documento = form.cleaned_data.get('numero_documento')

        if Instructor.objects.filter(numero_documento=numero_documento).exists():
            form.add_error('numero_documento', 'Ya existe un instructor registrado con este número de documento.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        success_url = reverse('app:instructor_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class InstructorUpdateView(UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'instructor/crear.html'
    success_url = reverse_lazy('app:instructor_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar instructor'
        context['entidad'] = 'Editar instructor'
        context['error'] = 'Este instructor ya está registrado'
        context['listar_url'] = reverse_lazy('app:instructor_lista')
        return context

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre').lower()
        response = super().form_valid(form)
        success_url = reverse('app:instructor_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class InstructorDeleteView(DeleteView):
    model = Instructor
    template_name = 'instructor/eliminar.html'
    success_url = reverse_lazy('app:instructor_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar instructor'
        context['entidad'] = 'Eliminar instructor'
        context['listar_url'] = reverse_lazy('app:instructor_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Instructor eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el instructor.'})