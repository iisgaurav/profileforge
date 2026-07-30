import pytest
from profileforge.core.config import ConfigLoader
from profileforge.core.exceptions import ConfigurationError

def test_config_loader_missing_file():
    with pytest.raises(ConfigurationError):
        ConfigLoader.load_main_config("nonexistent.yaml")

def test_theme_loader_missing_file():
    with pytest.raises(Exception):
        ConfigLoader.load_theme("missing-theme", "missing_dir")
