from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PhoneOtp

# Register your models here.

UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'avatar', 'bio')
UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active', 'is_staff', 'is_superuser', 'is_employee', 'is_customer', 'is_admin', 'is_supporter',
    'groups', 'user_permissions'
)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOtp)
