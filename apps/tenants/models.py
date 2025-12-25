from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
import uuid
from tenants.enums import TenantStatusChoices


class Client(TenantMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # TODO: Add onboarding_application field when onboarding app is created
    # onboarding_application = models.OneToOneField(
    #     "onboarding.OnboardingApplication", on_delete=models.PROTECT, null=True, blank=True
    # )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=TenantStatusChoices.choices,
        default=TenantStatusChoices.PENDING,
    )
    country_code = models.CharField(max_length=5, default="+234")
    base_currency = models.CharField(max_length=10, default="NGN")
    activated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True  # django-tenants will create schema automatically


class Domain(DomainMixin):
    """Domain routing for tenants"""

    pass
