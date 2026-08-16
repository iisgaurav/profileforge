__layer__ = "Layer 1 — Core"
class ProfileForgeError(Exception):
    """Base exception for ProfileForge"""


class ConfigurationError(ProfileForgeError):
    """Raised when there is an issue with the profileforge.yaml file"""


class ThemeError(ProfileForgeError):
    """Raised when a theme fails to load or parse"""





class ConnectorError(ProfileForgeError):
    """Raised when a connector fails to fetch required data"""
