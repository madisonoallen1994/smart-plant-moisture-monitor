# Hub (BLE Reader & HTTP Forwarder)

The hub is a **Python service** that bridges Bluetooth Low Energy (BLE) data from the plant probe to a backend over HTTP.

During early development and hardware testing, the hub runs locally on a laptop (macOS).  
In later phases, it is intended to run on a dedicated device (e.g. a Raspberry Pi).

---

## What this is

- A BLE → HTTP bridge
- Scans for a plant probe by name or address
- Reads raw sensor data from a BLE GATT characteristic
- Adds a hub-generated timestamp
- POSTs readings to a backend ingest endpoint

The hub is the integration layer between hardware and software.

---

## What this is NOT

- Not firmware (that lives in `firmware/`)
- Not a backend or database
- Not a UI or dashboard
- Not production-ready infrastructure

It is intentionally simple and debuggable.

---

## Folder structure

```text
hub/
├── src/                # Hub source code
│   ├── main.py         # Entry point
│   ├── config.py       # Environment variable loading
│   ├── ble_client.py   # BLE scanning and reads
│   ├── http_client.py  # HTTP POST logic
│   └── logger.py       # Logging setup
├── tests/              # Lightweight tests
├── logs/               # Runtime logs (created locally; not committed)
├── .env.example        # Example configuration
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Configuration

The hub is configured via environment variables.

An example file is provided in `.env.example`.  
For local runs or hardware day, this should be copied to `.env`.

Key variables include:

- `DRY_RUN` — Skip BLE and generate fake readings
- `BACKEND_INGEST_URL` — Where readings are POSTed
- `PROBE_NAME` / `PROBE_ADDRESS` — BLE device selection
- `SERVICE_UUID` / `CHAR_UUID` — BLE GATT contract
- `POLL_INTERVAL_SECONDS` — Read interval

## Local development (no hardware)

The hub supports a `DRY_RUN` mode that skips BLE entirely and generates fake readings.  
This is used to validate the full HTTP data flow without hardware.

From the repository root:
```bash
cd hub
source .venv/bin/activate
mkdir -p logs
PYTHONPATH=src python src/main.py
```
When DRY_RUN=true, the hub will:
- Skip BLE scanning and connection
- Generate a fake sensor reading
- POST it to the configured backend endpoint on each poll cycle

## Running with real BLE hardware

1. Set `DRY_RUN=false` in `.env`
2. Power on the probe and confirm it is advertising over BLE
3. Optionally set `PROBE_ADDRESS` for more reliable discovery
4. Start the hub using the same command as above

macOS BLE troubleshooting steps are documented in:  
`docs/runbooks/hardware_day_quick_start.md`

## Future direction

The hub may eventually:
- Run on a Raspberry Pi or similar device
- Support multiple probes
- Add retry or buffering logic
- Forward data to a cloud backend
For now, it is optimized for clarity, debuggability, and hardware-day reliability.

# Hello