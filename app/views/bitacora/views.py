from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from app.models import *
from app.forms import *

@method_decorator(never_cache, name='dispatch')
def lista_bitacoras(request):
    nombre = {
        'titulo': 'Registro de bitacoras realizados',
        'bitacoras': Bitacora.objects.all(),
    }
    return render(request, 'bitacora/listar.html', nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class BitacoraListView(ListView):
    model = Bitacora
    template_name = 'bitacora/listar.html'
    context_object_name = 'bitacoras'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Bitacoras realizados'
        context['entidad'] = 'Bitacoras realizados'
        context['listar_url'] = reverse_lazy('app:bitacora_lista')
        context['crear_url'] = reverse_lazy('app:bitacora_crear')

        bitacoras_con_elementos = []
        for bitacora in context['bitacoras']:
            detalles = bitacora.detalles.all()  
            bitacoras_con_elementos.append({
                'bitacora': bitacora,
                'elementos': detalles 
            })

        context['bitacoras_con_elementos'] = bitacoras_con_elementos
        return context

###### CREAR ######

@method_decorator(never_cache, name='dispatch')
class BitacoraCreateView(CreateView):
    template_name = 'bitacora/crear.html'
    form_class = BitacoraFormSet

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = BitacoraFormSet()
        context = {
            'form': form,
            'formset': formset,
            'titulo': 'Registrar nueva bitácora',
            'entidad': 'Registrar nueva bitácora',
            'aprendiz': Aprendiz.objects.all(),
            'listar_url': reverse_lazy('app:bitacora_crear'),
            'crear_url': reverse_lazy('app:bitacora_lista'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = BitacoraFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                bitacora = form.save()

                detalles = formset.save(commit=False)
                for detalle in detalles:
                    detalle.bitacora = bitacora 
                    detalle.save()

                return JsonResponse({'success': True, 'message': 'Bitacora registrada correctamente.'})

            except Exception as e:
                print(f"Error al guardar el bitacora: {e}")
                return JsonResponse({'success': False, 'errors': str(e)})

        else:
            errors = {
                'form_errors': form.errors.as_json(),
                'formset_errors': formset.errors.as_json(),
            }
            return JsonResponse({'success': False, 'errors': errors})
    
# ###### EDITAR ######

# @method_decorator(never_cache, name='dispatch')
# class BitacoraUpdateView(UpdateView):
#     model = Bitacora
#     form_class = BitacoraForm
#     template_name = 'bitacora/crear.html'
#     success_url = reverse_lazy('app:bitacora_lista')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Editar bitacora'
#         context['entidad'] = 'Editar bitacora'
#         context['error'] = 'Error al editar el bitacora.'
#         context['listar_url'] = reverse_lazy('app:bitacora_lista')
#         return context
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         success_url = reverse('app:bitacora_crear') + '?updated=True'
#         return redirect(success_url)

# ###### ELIMINAR ######

# @method_decorator(never_cache, name='dispatch')
# class BitacoraDeleteView(DeleteView):
#     model = Bitacora
#     template_name = 'bitacora/eliminar.html'
#     success_url = reverse_lazy('app:bitacora_lista')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Eliminar bitacora'
#         context['entidad'] = 'Eliminar bitacora'
#         context['listar_url'] = reverse_lazy('app:bitacora_lista')
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         try:
#             self.object.delete()
#             return JsonResponse({'success': True, 'message': 'Bitacora eliminado con éxito.'})
#         except ProtectedError:
#             return JsonResponse({'success': False, 'message': 'No se puede eliminar el bitacora.'})