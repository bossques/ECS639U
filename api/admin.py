from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom User Details',
            {
                'fields': (
                    'date_of_birth',
                    'profile_image',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
