from enum import Enum


class LeadStatus(str, Enum):
    """Lead status enum."""
    NEW = "new"
    CONTACT = "contact"
    QUALIFIED = "qualified"
    WON = "won"


class LeadSource(str, Enum):
    """Lead source enum."""
    WEBSITE = "website"
    PHONE = "phone"
    EMAIL = "email"
    REFERRAL = "referral"
    SOCIAL_MEDIA = "social_media"
    ADVERTISING = "advertising"
    OTHER = "other"