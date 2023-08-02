from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.translation import gettext_lazy as _

admin.site.register(ExperienceLevel)


@admin.register(User)
class CustomeUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "mobile", "pan_number", "pan_verified", "referal_code", "experience_point", "ex_level","image" )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )