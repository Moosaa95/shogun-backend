from django.urls import path
from onboarding.endpoints import (
    OnboardingCreateView,
    PromoteOnboardingAPIView,
    VerifyOnboardingAPIView,
)

urlpatterns = [
    path("create/", OnboardingCreateView.as_view(), name="onboarding-create"),
    path("promote/", PromoteOnboardingAPIView.as_view(), name="onboarding-promote"),
    path("verify/", VerifyOnboardingAPIView.as_view(), name="onboarding-verify"),
]
