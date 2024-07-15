from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
