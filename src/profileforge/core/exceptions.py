class ProfileForgeError(Exception):
    """Base exception for ProfileForge"""


class ConfigurationError(ProfileForgeError):
    """Raised when there is an issue with the profileforge.yaml file"""


class ThemeError(ProfileForgeError):
    """Raised when a theme fails to load or parse"""


class WidgetError(ProfileForgeError):
    """Raised when a widget encounters an error during rendering or loading"""


class RendererError(ProfileForgeError):
    """Raised when the layout engine or renderer fails"""


class ConnectorError(ProfileForgeError):
    """Raised when a connector fails to fetch required data"""
