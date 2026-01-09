import asyncio
import json
import os
from typing import Any, Optional

from bleak import BleakClient, BleakScanner


async def find_probe_address(
  probe_name: Optional[str],
  probe_address: Optional[str],
  logger
) -> str:
  if probe_address:
    logger.info(f'BLE identity: using configured PROBE_ADDRESS={probe_address}')
    return probe_address

  assert probe_name is not None

  scan_timeout_seconds = float(os.getenv("BLE_SCAN_TIMEOUT_SECONDS", "8.0"))
  logger.info(f'BLE identity: scanning up to {scan_timeout_seconds}s for PROBE_NAME="{probe_name}"')
  devices = await BleakScanner.discover(timeout=scan_timeout_seconds)

  for d in devices:
    name = (d.name or "").strip()

    if name == probe_name:
      logger.info(f'BLE identity: resolved address={d.address} name="{name}"')
      return d.address

  raise RuntimeError(
    f'Probe not found by name="{probe_name}". '
    f'Try increasing scan timeout or set PROBE_ADDRESS.'
  )


async def read_latest_reading(address: str, char_uuid: str, logger) -> dict[str, Any]:
  logger.info(f"BLE read: connect → read → disconnect address={address} char_uuid={char_uuid}")

  async with BleakClient(address, timeout=10.0) as client:
    if not client.is_connected:
      raise RuntimeError("BLE client failed to connect.")

    raw = await client.read_gatt_char(char_uuid)
    text = raw.decode("utf-8", errors="replace").strip()

    logger.info(f"BLE read: success address={address} char_uuid={char_uuid} bytes={len(raw)}")

    try:
      payload = json.loads(text)
      if not isinstance(payload, dict):
        raise ValueError("Characteristic JSON is not an object.")
      return payload
    except Exception as e:
      raise ValueError(f"Characteristic JSON parse failed: {e}") from e


async def poll_readings(address: str, char_uuid: str, interval_seconds: int, logger):
  while True:
    try:
      yield await read_latest_reading(address, char_uuid, logger)
    except Exception as e:
      logger.error(f"BLE read failed address={address} char_uuid={char_uuid} error={e}")
    await asyncio.sleep(interval_seconds)
