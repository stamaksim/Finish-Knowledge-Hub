from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from knowhub.models import User, Category, Services

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "category", "price"]
    list_filter = ["category"]
    search_fields = ["name"]

@admin.register(User)
class UsersAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
