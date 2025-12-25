from django.db.models import TextChoices


class UserRoles(TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    ACCOUNTANT = "accountant", "Accountant"
    VIEWER = "viewer", "Viewer"


class MembershipStatus(TextChoices):
    ACTIVE = "active", "Active"
    REVOKED = "revoked", "Revoked"
