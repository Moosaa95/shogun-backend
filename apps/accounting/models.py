from django.db import models
from django.db.models import SET_NULL
from django_ledger.models import EntityModel, LedgerModel
from commons.mixins import ModelMixin


class AccountingEntity(EntityModel):
    """Extends Django Ledger Entity with custom fields"""

    # Use proper choices that match django-ledger's expectations
    ACCOUNTING_METHOD_CASH = "cash"
    ACCOUNTING_METHOD_ACCRUAL = "accrual"
    ACCOUNTING_METHOD_CHOICES = [
        (ACCOUNTING_METHOD_CASH, "Cash"),
        (ACCOUNTING_METHOD_ACCRUAL, "Accrual"),
    ]

    accounting_method = models.CharField(
        max_length=20,
        choices=ACCOUNTING_METHOD_CHOICES,
        default=ACCOUNTING_METHOD_ACCRUAL,
    )

    class Meta:
        # Override parent Meta to fix indexes issue with 'admin' field
        indexes = []
        verbose_name = "Accounting Entity"
        verbose_name_plural = "Accounting Entities"


# class AccountingEntity(EntityModel):
#     """Extends Django Ledger Entity with custom fields"""

#     # TODO: Add business_entity field when BusinessEntity model is created
#     # business_entity = models.OneToOneField("BusinessEntity", on_delete=CASCADE, null=True, blank=True)
#     accounting_method = models.CharField(max_length=20)  # Cash, Accrual

#     class Meta:
#         # Override parent Meta to fix indexes issue with 'admin' field
#         indexes = []
#         verbose_name = "Accounting Entity"
#         verbose_name_plural = "Accounting Entities"


# class ExpenseCategory(ModelMixin):
#     """Custom expense categories for tax optimization"""

#     name = models.CharField(max_length=100)
#     tax_deductible = models.BooleanField(default=True)
#     deduction_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     coa_account = models.ForeignKey("django_ledger.AccountModel", on_delete=SET_NULL, null=True, blank=True)
