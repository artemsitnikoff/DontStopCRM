from enum import Enum


class MessageSenderType(str, Enum):
    """Message sender type enum."""
    CLIENT = "client"
    AGENT = "agent"
    SYSTEM = "system"