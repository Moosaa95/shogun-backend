# """
# Tenant-specific URL configuration.
# These URLs are accessible from tenant subdomains/domains.
# Includes both shared and tenant-specific apps.
# """

# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

# urlpatterns = [
#     # Admin (accessible from tenant schemas)
#     path("admin/", admin.site.urls),

#     # Shared APIs (also accessible from tenants)
#     path("api/v1/identity/", include("identity.urls")),
#     path("api/v1/onboarding/", include("onboarding.urls")),
#     path("api/v1/tenants/", include("tenants.urls")),

#     # Tenant-specific apps
#     path("ledger/", include("django_ledger.urls", namespace="django_ledger")),
#     path("api/v1/accounting/", include("accounting.urls")),

#     # API Documentation
#     path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
#     path(
#         "api/v1/schema/swagger-ui/",
#         SpectacularSwaggerView.as_view(url_name="schema"),
#         name="swagger-ui",
#     ),
#     path(
#         "api/v1/schema/redoc/",
#         SpectacularRedocView.as_view(url_name="schema"),
#         name="redoc",
#     ),
# ]

# project/urls_public.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin (public schema only)
    path("admin/", admin.site.urls),
    # Platform APIs
    path("api/v1/identity/", include("identity.urls")),
    path("api/v1/onboarding/", include("onboarding.urls")),
    path("api/v1/tenants/", include("tenants.urls")),  # promotion trigger lives here
    # API schema (public only)
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
