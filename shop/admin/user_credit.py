from django.contrib import admin

from shop.models import UserCredit


@admin.register(UserCredit)
class UserCreditAdmin(admin.ModelAdmin):
    """Admin for UserCredit model."""

    list_display = ("user", "credit")
    search_fields = ("user__username",)
    autocomplete_fields = ("user",)
