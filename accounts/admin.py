from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ApprenticeProfile, InstructorProfile

class ApprenticeProfileInline(admin.StackedInline):
    model = ApprenticeProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Aprendiz'

class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Instructor'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Tipo de Usuario', {'fields': ('user_type',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.user_type == 'apprentice':
                return [ApprenticeProfileInline]
            elif obj.user_type == 'instructor':
                return [InstructorProfileInline]
        return []

admin.site.register(User, CustomUserAdmin)
admin.site.register(ApprenticeProfile)
admin.site.register(InstructorProfile)
