import asyncio
import json
from typing import Any, Optional

from bleak import BleakClient, BleakScanner

async def find_probe_address(probe_name: Optional[str], probe_address: Optional[str], logger) -> str:
  if probe_address:
    logger.info(f'Using configured probe address: {probe_address}')
    return probe_address

  assert probe_name is not None

  logger.info(f'Scanning for probe name="{probe_name}"...')
  devices = await BleakScanner.discover(timeout=8.0)

  for d in devices:
    # d.name can be None
    if (d.name or "").strip() == probe_name:
      logger.info(f'Found probe: name="{d.name}" address={d.address} rssi={getattr(d, "rssi", None)}')
      return d.address

  raise RuntimeError(f'Probe not found by name: "{probe_name}". Try increasing timeout or set PROBE_ADDRESS.')

async def read_latest_reading(address: str, char_uuid: str, logger) -> dict[str, Any]:
  async with BleakClient(address, timeout=10.0) as client:
    if not client.is_connected:
      raise RuntimeError("BLE client failed to connect.")

    raw = await client.read_gatt_char(char_uuid)
    text = raw.decode("utf-8", errors="replace").strip()
    logger.info(f"Read char {char_uuid}: {text}")

    try:
      payload = json.loads(text)
      if not isinstance(payload, dict):
        raise ValueError("Characteristic JSON is not an object.")
      return payload
    except Exception as e:
      raise ValueError(f"Failed to parse characteristic JSON: {e}") from e

async def poll_readings(address: str, char_uuid: str, interval_seconds: int, logger):
  while True:
    try:
      yield await read_latest_reading(address, char_uuid, logger)
    except Exception as e:
      logger.error(f"BLE read failed: {e}")
    await asyncio.sleep(interval_seconds)
