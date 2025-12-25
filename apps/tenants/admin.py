from django_tenants.admin import TenantAdminMixin
from django.contrib import admin

from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("schema_name", "status", "country_code", "base_currency", "created_at")
    search_fields = ("schema_name", "country_code")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")
    search_fields = ("domain", "tenant__name")
