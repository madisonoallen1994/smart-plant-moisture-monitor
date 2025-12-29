import logging
from logging.handlers import RotatingFileHandler

def setup_logger(level: str, log_file: str) -> logging.Logger:
  logger = logging.getLogger("hub")
  logger.setLevel(level.upper())
  logger.propagate = False

  if logger.handlers:
    return logger

  formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
  )

  ch = logging.StreamHandler()
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
  fh.setFormatter(formatter)
  logger.addHandler(fh)

  return logger
