import asyncio
from hub.src.config import load_config
from hub.src.logger import setup_logger
from hub.src.ble_client import find_probe_address, poll_readings
from hub.src.http_client import post_reading

async def dry_run_loop(cfg, logger):
  fake = {"probeId": "probe-001", "moistureRaw": 500, "fwVersion": "0.1.0"}
  while True:
    try:
      post_reading(cfg.backend_ingest_url, fake, logger)
    except Exception as e:
      logger.error(f"Dry run POST failed: {e}")
    await asyncio.sleep(cfg.poll_interval_seconds)

async def run():
  cfg = load_config()
  logger = setup_logger(cfg.log_level, cfg.log_file)

  logger.info("Hub service starting")
  logger.info(f"dry_run={cfg.dry_run} backend={cfg.backend_ingest_url}")

  if cfg.dry_run:
    await dry_run_loop(cfg, logger)
    return

  address = await find_probe_address(cfg.probe_name, cfg.probe_address, logger)

  async for reading in poll_readings(address, cfg.char_uuid, cfg.poll_interval_seconds, logger):
    try:
      post_reading(cfg.backend_ingest_url, reading, logger)
    except Exception as e:
      logger.error(f"POST failed: {e}")

def main():
  asyncio.run(run())

if __name__ == "__main__":
  main()
