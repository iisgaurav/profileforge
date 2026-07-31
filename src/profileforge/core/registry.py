from typing import Callable

WIDGET_REGISTRY: dict[str, type] = {}
ConnectorRegistry: dict[str, type] = {}


def register_widget(name: str) -> Callable:
    def wrapper(cls):
        WIDGET_REGISTRY[name] = cls
        return cls

    return wrapper


def register_connector(name: str) -> Callable:
    def wrapper(cls):
        ConnectorRegistry[name] = cls
        return cls

    return wrapper
