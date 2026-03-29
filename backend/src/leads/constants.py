from enum import Enum


class LeadStatus(str, Enum):
    """Lead status enum."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    WON = "won"


class LeadSource(str, Enum):
    """Lead source enum."""
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    PHONE = "phone"