from django.db.models import TextChoices


class BusinessTypeChoices(TextChoices):
    SOLE_PROPRIETORSHIP = "SOLE_PROPRIETORSHIP", "Sole Proprietorship"
    PARTNERSHIP = "PARTNERSHIP", "Partnership"
    CORPORATION = "CORPORATION", "Corporation"
    LLC = "LLC", "Limited Liability Company"
    NON_PROFIT = "NON_PROFIT", "Non-Profit Organization"


class BusinessStatusChoices(TextChoices):
    DRAFT = "DRAFT", "Draft"
    UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
    VERIFIED = "VERIFIED", "Verified"
    REJECTED = "REJECTED", "Rejected"
    SUBMITTED = "SUBMITTED", "Submitted"
    PROMOTED = "PROMOTED", "Promoted"
