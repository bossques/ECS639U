from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ArticleCategory, Article, ArticleComment


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
                    'favourite_categories'
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(ArticleComment)

