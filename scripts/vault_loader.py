"""Zero-Leak credential loader for HubHum.

Priority order:
1. Local PCP Vault (.pcp/vault.local.jsonl)
2. Local .env file (gitignored)
3. Process environment variables (GitHub Actions Secrets)
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VAULT_PATH = PROJECT_ROOT / ".pcp" / "vault.local.jsonl"
ENV_PATH = PROJECT_ROOT / ".env"
EVENTS_LOG_PATH = PROJECT_ROOT / ".pcp" / "context" / "events.log"

PLACEHOLDER_PREFIX = "PASTE_"


def _is_usable_secret(value: str | None) -> bool:
    """Return True if value is non-empty and not an unedited template placeholder."""
    if not value:
        return False
    cleaned = value.strip()
    if not cleaned:
        return False
    return not (cleaned.startswith(PLACEHOLDER_PREFIX) and cleaned.endswith("_HERE"))


def _log_vault_access(key_name: str, source: str, secret_value: str) -> None:
    """Append SHA-256 audited access entry to .pcp/context/events.log (never plaintext)."""
    if not EVENTS_LOG_PATH.parent.exists():
        return
    digest = hashlib.sha256(secret_value.encode("utf-8")).hexdigest()
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": "VAULT_ACCESS",
        "key": key_name,
        "source": source,
        "sha256": digest,
    }
    try:
        with EVENTS_LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def _read_vault_entries() -> dict[str, dict]:
    """Parse .pcp/vault.local.jsonl entries indexed by id."""
    entries: dict[str, dict] = {}
    if not VAULT_PATH.exists():
        return entries
    for raw_line in VAULT_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict) and obj.get("id") and obj.get("rotated") is None:
                entries[obj["id"]] = obj
        except json.JSONDecodeError:
            continue
    return entries


def _read_dotenv() -> dict[str, str]:
    """Read local .env key=value pairs without external dependencies."""
    values: dict[str, str] = {}
    if not ENV_PATH.exists():
        return values
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def get_secret(vault_id: str, vault_field: str, env_var: str) -> str | None:
    """Retrieve a secret cleanly across Vault -> .env -> Environment."""
    entries = _read_vault_entries()
    entry = entries.get(vault_id)
    if entry and isinstance(entry.get("data"), dict):
        candidate = entry["data"].get(vault_field)
        if _is_usable_secret(candidate):
            _log_vault_access(vault_id, "vault.local.jsonl", candidate)
            return candidate.strip()

    dotenv = _read_dotenv()
    env_candidate = dotenv.get(env_var)
    if _is_usable_secret(env_candidate):
        _log_vault_access(env_var, ".env", env_candidate)  # type: ignore[arg-type]
        return env_candidate.strip()  # type: ignore[union-attr]

    os_candidate = os.environ.get(env_var)
    if _is_usable_secret(os_candidate):
        _log_vault_access(env_var, "os.environ", os_candidate)  # type: ignore[arg-type]
        return os_candidate.strip()  # type: ignore[union-attr]

    return None


def get_all_runtime_keys() -> dict[str, str | None]:
    """Return runtime API keys without ever printing or logging values."""
    return {
        "GEMINI_API_KEY": get_secret("ai.gemini", "api_key", "GEMINI_API_KEY"),
        "GROQ_API_KEY": get_secret("ai.groq", "api_key", "GROQ_API_KEY"),
        "GITHUB_TOKEN": get_secret("dev.github", "pat", "GITHUB_TOKEN"),
    }


def main() -> None:
    keys = get_all_runtime_keys()
    status = {k: ("CONFIGURED" if v else "MISSING_OR_PLACEHOLDER") for k, v in keys.items()}
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
