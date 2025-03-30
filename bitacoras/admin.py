from django.contrib import admin
from .models import Bitacora

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'apprentice', 'upload_date')
    list_filter = ('upload_date', 'apprentice')
    search_fields = ('filename', 'apprentice__username', 'apprentice__first_name', 'apprentice__last_name')
    date_hierarchy = 'upload_date'
