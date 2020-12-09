from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    """Кастомная административная панель"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_expert')
    list_filter = ('is_staff', 'is_active', 'is_expert')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'middle_name')}),
        ('Права доступа', {'fields': ('is_superuser', 'is_staff', 'is_active', 'is_expert')}),
        ('Важные даты', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'password1', 'password2', 'last_name', 'first_name',
                    'middle_name', 'is_superuser', 'is_staff', 'is_active', 'is_expert'
                    )
            }
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
