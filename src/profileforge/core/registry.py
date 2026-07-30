from typing import Callable, Dict, Any, Type

WIDGET_REGISTRY: Dict[str, Type] = {}
DATASOURCE_REGISTRY: Dict[str, Type] = {}

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
