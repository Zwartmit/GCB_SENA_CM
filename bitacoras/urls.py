from django.urls import path
from . import views

app_name = 'bitacoras'

urlpatterns = [
    # Apprentice URLs
    path('list/', views.list_bitacoras, name='list_bitacoras'),
    path('upload/', views.upload_bitacora, name='upload_bitacora'),
    path('delete/<int:pk>/', views.delete_bitacora, name='delete_bitacora'),
    
    # Instructor URLs
    path('apprentices/', views.apprentice_list, name='apprentice_list'),
    path('apprentices/<int:apprentice_id>/bitacoras/', views.apprentice_bitacoras, name='apprentice_bitacoras'),
    path('link-apprentice/', views.link_apprentice, name='link_apprentice'),
    path('unlink-apprentice/<int:apprentice_id>/', views.unlink_apprentice, name='unlink_apprentice'),
]
