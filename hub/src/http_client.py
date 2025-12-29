import datetime
import requests

def iso_now_utc() -> str:
  return datetime.datetime.now(datetime.timezone.utc).isoformat()

def post_reading(backend_url: str, reading_from_probe: dict, logger) -> None:
  # v0 contract: hub -> backend
  payload = {
    "probeId": reading_from_probe.get("probeId"),
    "timestamp": iso_now_utc(),
    "moistureRaw": reading_from_probe.get("moistureRaw"),
    "fwVersion": reading_from_probe.get("fwVersion"),
  }

  # Optional
  if "batteryMv" in reading_from_probe and reading_from_probe.get("batteryMv") is not None:
    payload["batteryMv"] = reading_from_probe.get("batteryMv")

  logger.info(f"POST {backend_url} payload={payload}")
  resp = requests.post(backend_url, json=payload, timeout=10)
  logger.info(f"Backend response: {resp.status_code}")
  resp.raise_for_status()
