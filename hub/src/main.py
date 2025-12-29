import asyncio
from config import load_config
from logger import setup_logger
from ble_client import find_probe_address, poll_readings
from http_client import post_reading


async def dry_run_loop(cfg, logger):
  fake = {"probeId": "probe-001", "moistureRaw": 500, "fwVersion": "0.1.0"}
  cycle = 0

  while True:
    cycle += 1
    logger.info(f"Poll cycle start mode=dry_run cycle={cycle}")
    try:
      post_reading(cfg.backend_ingest_url, fake, logger)
    except Exception as e:
      logger.error(f"Dry run POST failed cycle={cycle} error={e}")
    logger.info(f"Poll cycle end mode=dry_run cycle={cycle}")
    await asyncio.sleep(cfg.poll_interval_seconds)


async def run():
  cfg = load_config()
  logger = setup_logger(cfg.log_level, cfg.log_file)

  logger.info("Hub service starting")
  logger.info(f"Config dry_run={cfg.dry_run} backend={cfg.backend_ingest_url} poll_interval_seconds={cfg.poll_interval_seconds}")

  if cfg.dry_run:
    await dry_run_loop(cfg, logger)
    return

  address = await find_probe_address(cfg.probe_name, cfg.probe_address, logger)
  cycle = 0

  async for reading in poll_readings(address, cfg.char_uuid, cfg.poll_interval_seconds, logger):
    cycle += 1
    logger.info(f"Poll cycle start mode=ble cycle={cycle} address={address} char_uuid={cfg.char_uuid}")
    try:
      post_reading(cfg.backend_ingest_url, reading, logger)
    except Exception as e:
      logger.error(f"POST failed cycle={cycle} address={address} error={e}")
    logger.info(f"Poll cycle end mode=ble cycle={cycle} address={address}")


def main():
  asyncio.run(run())


if __name__ == "__main__":
  main()
