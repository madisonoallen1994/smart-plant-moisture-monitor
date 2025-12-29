# Hub Source Code

This folder contains the **implementation of the hub service**.

The hub connects to the plant probe over Bluetooth Low Energy (BLE), reads sensor data, and forwards readings to a backend over HTTP.

This code is intended to be readable, debuggable, and easy to modify during early development.

---

## Entry point

The main entry point is:

```text
main.py
```
This file:
- Loads configuration from environment variables
- Initializes logging
- Chooses between DRY_RUN mode and real BLE mode
- Runs the main polling loop


## Module overview 
```text
src/
├── main.py        # Service entry point and main loop
├── config.py      # Environment variable loading and validation
├── ble_client.py  # BLE scanning, connection, and characteristic reads
├── http_client.py # HTTP client for posting readings
├── logger.py      # Logging configuration
└── __init__.py
```

## Data flow

At a high level, the hub performs the following steps:
1. Load configuration from .env
2. Discover the plant probe over BLE (or skip in DRY_RUN mode)
3. Read the latest sensor value from the GATT characteristic
4. Construct a reading payload
5. POST the payload to the configured backend endpoint
6. Sleep until the next poll cycle
Each step is intentionally isolated in its own module.

## DRY_RUN mode

When DRY_RUN=true:
- BLE scanning and connection are skipped
- A fake sensor reading is generated
- The rest of the data flow is unchanged
This allows HTTP and backend logic to be tested independently of hardware.

## Error handling and logging

- Errors are logged to both stdout and rotating log files
- Logging behavior is configured via environment variables
- The hub is designed to fail loudly rather than silently during development
Log files are written to hub/logs/.

## Development guidelines

When modifying this code:
- Prefer clarity over optimization
- Keep BLE logic isolated to ble_client.py
- Avoid embedding configuration directly in code
- Update runbooks if behavior changes
The goal is to keep this code understandable by someone new to the project.

## Relationship to the rest of the system

- Firmware exposes data over BLE
- Hub source (this folder) reads and forwards that data
- Backend stub receives and logs readings locally
- Docs explain how to run and debug the system
This folder sits at the center of the integration flow.