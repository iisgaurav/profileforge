from typing import Callable

WIDGET_REGISTRY: dict[str, type] = {}
DATASOURCE_REGISTRY: dict[str, type] = {}


def register_widget(name: str) -> Callable:
    def wrapper(cls):
        WIDGET_REGISTRY[name] = cls
        return cls

    return wrapper


def register_datasource(name: str) -> Callable:
    def wrapper(cls):
        DATASOURCE_REGISTRY[name] = cls
        return cls

    return wrapper
