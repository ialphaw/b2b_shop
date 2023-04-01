from django.contrib import admin

from shop.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction model."""
    
    list_display = ("user", "amount", "get_category_display")
    search_fields = ("user__username",)
    autocomplete_fields = ("user",)
