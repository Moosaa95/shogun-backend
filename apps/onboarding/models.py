from django.db import models
from commons.mixins import ModelMixin
from onboarding.enums import BusinessStatusChoices


class OnboardingApplication(ModelMixin):
    initiated_by = models.ForeignKey(
        "identity.User", on_delete=models.PROTECT, related_name="onboarding_apps"
    )
    country_code = models.CharField(max_length=5)  # NG, US, etc
    business_name = models.CharField(max_length=255)
    business_profile = models.JSONField()  # snapshot of submitted data
    identifiers = models.JSONField()  # CAC, TIN, EIN, etc
    status = models.CharField(
        max_length=20,
        choices=BusinessStatusChoices.choices,
        default=BusinessStatusChoices.DRAFT,
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    promoted_at = models.DateTimeField(null=True, blank=True)

    def can_promote(self):
        return self.status == BusinessStatusChoices.VERIFIED

    def __str__(self):
        return f"OnboardingApplication({self.business_name}, {self.country_code}, {self.status})"

    class Meta:
        verbose_name = "Onboarding Application"
        verbose_name_plural = "Onboarding Applications"

    @classmethod
    def create_application(cls, **kwargs):
        application = cls.objects.create(**kwargs)
        return application
