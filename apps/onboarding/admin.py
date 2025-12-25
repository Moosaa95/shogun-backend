from django.contrib import admin
from onboarding.models import OnboardingApplication


# Register your models here.
@admin.register(OnboardingApplication)
class OnboardingApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "business_name", "initiated_by", "status", "created_at")
    search_fields = ("business_name", "initiated_by__email")
    list_filter = ("status", "created_at")
