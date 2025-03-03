from django.urls import path
from django.conf.urls.static import static
from pseep import settings
from app.views import *
from app.views.aprendiz.views import *
from app.views.instructor.views import *
from app.views.bitacora.views import *

app_name = 'app'
urlpatterns = [
    path('aprendiz/listar/', AprendizListView.as_view(), name='aprendiz_lista'),
    path('aprendiz/crear/', AprendizCreateView.as_view(), name='aprendiz_crear'),
    path('aprendiz/editar/<int:pk>/', AprendizUpdateView.as_view(), name='aprendiz_editar'),
    path('aprendiz/eliminar/<int:pk>/', AprendizDeleteView.as_view(), name='aprendiz_eliminar'),
    path('aprendiz/perfil/', PerfilAprendiz.as_view(), name='perfil_aprendiz'),
    
    path('instructor/listar/', InstructorListView.as_view(), name='instructor_lista'),
    path('instructor/crear/', InstructorCreateView.as_view(), name='instructor_crear'),
    path('instructor/editar/<int:pk>/', InstructorUpdateView.as_view(), name='instructor_editar'),
    path('instructor/eliminar/<int:pk>/', InstructorDeleteView.as_view(), name='instructor_eliminar'),
    
    # path('empresa/listar/', EmpresaListView.as_view(), name='empresa_lista'),
    # path('empresa/crear/', EmpresaCreateView.as_view(), name='empresa_crear'),
    
    path('bitacora/listar/', BitacoraListView.as_view(), name='bitacora_lista'),
    path('bitacora/crear/', BitacoraCreateView.as_view(), name='bitacora_crear'),
    # path('editar-perfil/', editar_perfil_aprendiz, name='editar_perfil_aprendiz'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
