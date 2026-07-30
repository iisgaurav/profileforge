class ProfileForgeError(Exception):
    """Base exception for ProfileForge"""
    pass

class ConfigurationError(ProfileForgeError):
    """Raised when there is an issue with the profileforge.yaml file"""
    pass

class ThemeError(ProfileForgeError):
    """Raised when a theme fails to load or parse"""
    pass

class WidgetError(ProfileForgeError):
    """Raised when a widget encounters an error during rendering or loading"""
    pass

class RendererError(ProfileForgeError):
    """Raised when the layout engine or renderer fails"""
    pass

class DataSourceError(ProfileForgeError):
    """Raised when a datasource fails to fetch required data"""
    pass
