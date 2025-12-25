import uuid
from django.db import transaction
from django.utils import timezone
from django_tenants.utils import schema_context

from onboarding.models import OnboardingApplication
from onboarding.enums import BusinessStatusChoices as OnboardingStatus
from tenants.models import Client, Domain
from tenants.enums import TenantStatusChoices as TenantStatus
from identity.models import Membership
from identity.enums import UserRoles as TenantRole

from django_ledger.models import LedgerModel, EntityModel
from django_ledger.models.chart_of_accounts import ChartOfAccountModel

from accounting.models import AccountingEntity


class VerificationError(Exception):
    pass


def verify_onboarding(onboarding_id: uuid.UUID) -> OnboardingApplication:
    with transaction.atomic():
        onboarding = OnboardingApplication.objects.select_for_update().get(
            id=onboarding_id
        )

        if onboarding.status != OnboardingStatus.DRAFT:
            raise VerificationError("Only draft onboardings can be verified")

        onboarding.status = OnboardingStatus.VERIFIED
        onboarding.verified_at = timezone.now()
        onboarding.save(update_fields=["status", "verified_at"])

        return onboarding


class PromotionError(Exception):
    pass


def promote_onboarding(onboarding_id: uuid.UUID) -> Client:

    with transaction.atomic():
        onboarding = OnboardingApplication.objects.select_for_update().get(
            id=onboarding_id
        )

        if onboarding.status != OnboardingStatus.VERIFIED:
            raise PromotionError("Onboarding must be verified before promotion")

        if onboarding.promoted_at:
            raise PromotionError("Onboarding already promoted")

        # schema_name = f"tenant_{onboarding.business_name.lower().replace(' ', '_')}_{str(uuid.uuid4())[:8]}"
        schema_name = onboarding.business_name.lower().strip()

        tenant = Client.objects.create(
            schema_name=schema_name,
            name=onboarding.business_name,
            status=TenantStatus.ACTIVE,
            country_code=onboarding.country_code,
            activated_at=timezone.now(),
        )

        Domain.objects.create(
            tenant=tenant,
            domain=f"{schema_name}.8c69a3ad3a25.ngrok-free.app",
            is_primary=True,
        )

        # MEMBERSHIP
        Membership.objects.create(
            user=onboarding.initiated_by,
            tenant=tenant,
            role=TenantRole.OWNER,
        )

        with schema_context(schema_name):
            entity = EntityModel.create_entity(
                name=onboarding.business_name,
                admin=onboarding.initiated_by,
                use_accrual_method=True,
                fy_start_month=1,
            )
            coa = entity.create_chart_of_accounts(
                coa_name=f"{entity.name} Default CoA",
                assign_as_default=True,
                commit=True,
            )

            coa.mark_as_active(commit=True)

            LedgerModel.objects.create(
                name="Primary General Ledger",
                entity=entity,
                posted=True,
            )

        # MARK ONBOARDING AS PROMOTED
        onboarding.status = OnboardingStatus.PROMOTED
        onboarding.promoted_at = timezone.now()
        onboarding.save(update_fields=["status", "promoted_at"])

        return tenant
