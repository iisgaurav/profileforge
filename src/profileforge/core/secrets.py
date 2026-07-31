import os
from typing import Optional


class SecretStore:
    """Provides access to secure credentials/tokens."""

    @classmethod
    def get(cls, key: str) -> Optional[str]:
        return os.environ.get(key)
