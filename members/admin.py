from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MemberProfile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MemberProfile
    list_display = ('username', 'is_staff', 'is_active', )
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'username', 'photo')}),
        ('Corporate Settings', {'fields': ('department', 'position', 'items_per_page')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_developer', 'is_seller')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_developer', 'is_seller' , 'photo')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

    list_display = ('id', 'first_name', 'last_name', 'username','is_developer', 'is_seller',)
    #list_display = ('id', 'email', 'is_developer', 'is_seller')

admin.site.register(MemberProfile, CustomUserAdmin)