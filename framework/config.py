from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_DIR = ROOT_DIR / "config" / "env"
SUPPORTED_ENVS = {"test", "preprod", "prod"}


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    """Parse simple key-value yaml (no nesting), enough for env config."""
    data: dict[str, Any] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value.isdigit():
            data[key] = int(value)
        else:
            data[key] = value.strip('"').strip("'")

    return data


def load_env_config(env_name: str) -> dict[str, Any]:
    normalized_env = env_name.strip().lower()
    if normalized_env not in SUPPORTED_ENVS:
        raise ValueError(
            f"Unsupported env '{env_name}'. Supported values: {sorted(SUPPORTED_ENVS)}"
        )

    env_file = ENV_DIR / f"{normalized_env}.yaml"
    if not env_file.exists():
        raise FileNotFoundError(f"Env config not found: {env_file}")

    data = _parse_simple_yaml(env_file)
    if "base_url" not in data:
        raise KeyError(f"'base_url' is required in {env_file}")

    return data
