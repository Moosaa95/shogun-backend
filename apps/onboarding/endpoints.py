from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from onboarding.serializers import (
    OnboardingCreateSerializer,
    PromotionRequestSerializer,
    VerificationRequestSerializer,
)
from onboarding.services.promotion import (
    promote_onboarding,
    PromotionError,
    VerificationError,
    verify_onboarding,
)


class OnboardingCreateView(APIView):
    """
    API endpoint to create a new onboarding application.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=OnboardingCreateSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "application_id": {"type": "string"},
                    "business_name": {"type": "string"},
                    "status": {"type": "string"},
                },
                "example": {
                    "message": "Onboarding application created successfully!",
                    "application_id": "123e4567-e89b-12d3-a456-426614174000",
                    "business_name": "Acme Corp",
                    "status": "DRAFT",
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "array", "items": {"type": "string"}},
                },
                "example": {
                    "status": "error",
                    "message": [
                        "initiated_by: This field is required.",
                        "country_code: This field is required.",
                        "business_name: This field is required.",
                    ],
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
                "example": {
                    "detail": "Authentication credentials were not provided.",
                },
            },
        },
        tags=["Onboarding"],
        summary="Create onboarding application",
        description="""
        Creates a new onboarding application for a business.

        The application status will be set to 'DRAFT' by default.

        **Required fields:**
        - initiated_by: UUID of the user creating the application
        - country_code: ISO country code (e.g., NG, US, UK)
        - business_name: Legal name of the business
        - business_profile: JSON object containing business details (must include 'business_type' and 'industry')
        - identifiers: JSON object with business registration numbers
        """,
    )
    def post(self, request):
        """
        Handle POST request to create onboarding application.
        """
        serializer = OnboardingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application = serializer.save()

        return Response(
            {
                "message": "Onboarding application created successfully!",
                "application_id": str(application.id),
                "business_name": application.business_name,
                "status": application.status,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyOnboardingAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerificationRequestSerializer,
        tags=["Onboarding"],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "application_id": {"type": "string"},
                    "status": {"type": "string"},
                    "verified_at": {"type": "string", "format": "date-time"},
                },
                "example": {
                    "application_id": "123e4567-e89b-12d3-a456-426614174000",
                    "status": "VERIFIED",
                    "verified_at": "2024-01-01T12:00:00Z",
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
                "example": {
                    "detail": "Only draft onboardings can be verified",
                },
            },
        },
        summary="Verify onboarding application",
        description="""
        Verifies a draft onboarding application.

        **Required fields:**
        - onboarding_id: UUID of the onboarding application to verify
        """,
    )
    def post(self, request):
        serializer = VerificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        onboarding_id = serializer.validated_data["onboarding_id"]

        try:
            onboarding = verify_onboarding(onboarding_id)
        except VerificationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "application_id": str(onboarding.id),
                "status": onboarding.status,
                "verified_at": onboarding.verified_at,
            },
            status=status.HTTP_200_OK,
        )


class PromoteOnboardingAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PromotionRequestSerializer,
        tags=["Onboarding"],
        responses={
            201: {
                "type": "object",
                "properties": {
                    "tenant_id": {"type": "string"},
                    "schema": {"type": "string"},
                    "status": {"type": "string"},
                },
                "example": {
                    "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                    "schema": "tenant_123e4567e8",
                    "status": "ACTIVE",
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
                "example": {
                    "detail": "Onboarding must be verified before promotion",
                },
            },
        },
        summary="Promote onboarding application",
        description="""
        Promotes a verified onboarding application to an active tenant. 
        **Required fields:**
        - onboarding_id: UUID of the onboarding application to promote
        """,
    )
    def post(self, request):
        serializer = PromotionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        onboarding_id = serializer.validated_data["onboarding_id"]

        try:
            tenant = promote_onboarding(onboarding_id)
        except PromotionError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "tenant_id": str(tenant.id),
                "schema": tenant.schema_name,
                "status": tenant.status,
            },
            status=status.HTTP_201_CREATED,
        )
