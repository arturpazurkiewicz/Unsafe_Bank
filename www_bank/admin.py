from django.contrib import admin

# Register your models here.
from www_bank.models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


admin.site.register(Account)
admin.site.register(TransferHistory)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username','password')}),
        (_('Personal info'), {'fields': (
            'email', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username','email','first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('username','email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username','email' ,'first_name', 'last_name')
    ordering = ('username',)