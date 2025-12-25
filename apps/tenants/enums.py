from django.db.models import TextChoices


class TenantStatusChoices(TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"
    PENDING = "PENDING", "Pending"
    CLOSED = "CLOSED", "Closed"
