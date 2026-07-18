from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser, Quiz
from .models import Question
from .models import Result

admin.site.register(Result)
admin.site.register(Question)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {
            "fields": ("role",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("role",),
        }),
    )

    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    admin.site.register(Quiz)
