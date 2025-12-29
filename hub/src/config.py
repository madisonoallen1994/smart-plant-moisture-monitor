from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

def _get_bool(key: str, default: bool) -> bool:
  raw = os.getenv(key)
  if raw is None:
    return default
  return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Config:
  backend_ingest_url: str
  probe_name: Optional[str]
  probe_address: Optional[str]
  service_uuid: str
  char_uuid: str
  poll_interval_seconds: int
  log_level: str
  log_file: str
  dry_run: bool


def load_config() -> Config:
  backend_ingest_url = os.getenv("BACKEND_INGEST_URL", "http://localhost:3000/api/v0/readings")
  probe_name = os.getenv("PROBE_NAME")
  probe_address = os.getenv("PROBE_ADDRESS")
  service_uuid = os.getenv("SERVICE_UUID", "")
  char_uuid = os.getenv("CHAR_UUID", "")
  poll_interval_seconds = int(os.getenv("POLL_INTERVAL_SECONDS", "10"))
  log_level = os.getenv("LOG_LEVEL", "INFO")
  log_file = os.getenv("LOG_FILE", "hub/logs/hub.log")
  dry_run = _get_bool("DRY_RUN", False)

  if not service_uuid or not char_uuid:
    raise ValueError("SERVICE_UUID and CHAR_UUID must be set in the environment.")

  # v0 sanity: require at least one filter to avoid random BLE device noise
  if not probe_name and not probe_address and not dry_run:
    raise ValueError("Set PROBE_NAME or PROBE_ADDRESS (or set DRY_RUN=true).")

  return Config(
    backend_ingest_url=backend_ingest_url,
    probe_name=probe_name,
    probe_address=probe_address,
    service_uuid=service_uuid,
    char_uuid=char_uuid,
    poll_interval_seconds=poll_interval_seconds,
    log_level=log_level,
    log_file=log_file,
    dry_run=dry_run,
  )
