from enum import Enum


class MessageDirection(str, Enum):
    """Message direction enum."""
    IN = "in"    # from client
    OUT = "out"  # to client


class MessageSource(str, Enum):
    """Message source enum."""
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    MANUAL = "manual"


DEFAULT_CHAT_PAGE_SIZE = 50