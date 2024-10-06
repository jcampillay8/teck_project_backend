from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define los campos a mostrar en la lista de usuarios en el admin
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    # Campos que se mostrarán en el formulario de creación de un usuario en el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )

    # Campos que se mostrarán al editar un usuario existente en el admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Usa el campo 'email' como el identificador para autenticación
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None

# Registra el modelo CustomUser en el admin con la configuración personalizada
admin.site.register(CustomUser, CustomUserAdmin)
