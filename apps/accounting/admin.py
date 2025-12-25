from django.contrib import admin
from accounting.models import AccountingEntity


# Register your models here.
@admin.register(AccountingEntity)
class AccountingEntityAdmin(admin.ModelAdmin):
    list_display = ("accounting_method",)
    search_fields = ("accounting_method",)
