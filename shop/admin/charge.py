from django.contrib import admin

from shop.models import Charge


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    """Admin for Charge model."""

    list_display = ("name", "amount", "is_active")
    search_fields = ("name",)
