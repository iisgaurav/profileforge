__layer__ = "Layer 1 — Core"
import os
from typing import Optional


class SecretStore:
    """Provides access to secure credentials/tokens."""

    @classmethod
    def get(cls, key: str) -> Optional[str]:
        if key in os.environ:
            return os.environ[key]

        env_path = os.path.join(os.getcwd(), ".env")
        if not os.path.exists(env_path):
            env_path = os.path.join(os.getcwd(), "..", ".env")

        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            k, v = line.split("=", 1)
                            if k.strip() == key:
                                v = v.strip()
                                if (v.startswith('"') and v.endswith('"')) or (
                                    v.startswith("'") and v.endswith("'")
                                ):
                                    v = v[1:-1]
                                return v
        return None
