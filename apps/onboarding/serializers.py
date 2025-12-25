from rest_framework import serializers
from .models import OnboardingApplication


class OnboardingCreateSerializer(serializers.Serializer):
    """
    Serializer for creating onboarding applications.
    Uses base Serializer instead of ModelSerializer for custom validation.
    """

    initiated_by = serializers.UUIDField(
        required=True, help_text="User ID of the initiator"
    )
    country_code = serializers.CharField(
        max_length=5,
        help_text="Country code (e.g., NG, US, UK)",
    )
    business_name = serializers.CharField(
        max_length=255,
        help_text="Legal business name",
    )
    business_profile = serializers.JSONField(
        help_text="Business profile data including type, industry, etc.",
    )
    identifiers = serializers.JSONField(
        help_text="Business identifiers like CAC, TIN, EIN, etc.",
    )

    def validate_country_code(self, value):
        """Validate country code format."""
        if not value or len(value) < 2:
            raise serializers.ValidationError("Invalid country code.")
        return value.upper()

    def validate_business_profile(self, value):
        """Validate business_profile JSON structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Business profile must be a JSON object.")

        # Optional: Check for required fields in business_profile
        required_fields = ["business_type", "industry"]
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(
                    f"Business profile must contain '{field}' field."
                )

        return value

    def validate_identifiers(self, value):
        """Validate identifiers JSON structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Identifiers must be a JSON object.")

        # Ensure at least one identifier is provided
        if not value:
            raise serializers.ValidationError(
                "At least one business identifier is required."
            )

        return value

    def validate_initiated_by(self, value):
        """Validate that the user exists."""
        from identity.models import User

        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")

        return user

    def create(self, validated_data):
        """Create a new OnboardingApplication instance."""
        application = OnboardingApplication.create_application(**validated_data)
        return application


class OnboardingResponseSerializer(serializers.Serializer):
    """Serializer for onboarding application response."""

    id = serializers.UUIDField(read_only=True)
    business_name = serializers.CharField()
    country_code = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class PromotionRequestSerializer(serializers.Serializer):
    """Serializer for promoting onboarding application request."""

    onboarding_id = serializers.UUIDField(
        required=True, help_text="UUID of the onboarding application to promote"
    )


class VerificationRequestSerializer(serializers.Serializer):
    """Serializer for verifying onboarding application request."""

    onboarding_id = serializers.UUIDField(
        required=True, help_text="UUID of the onboarding application to verify"
    )
