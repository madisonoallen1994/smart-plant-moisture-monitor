# Hub (Python)

This service runs on the Raspberry Pi hub and bridges BLE → HTTP.

- Scans for the probe (name or address)
- Reads the latest reading via BLE GATT characteristic
- Adds a hub-generated timestamp
- POSTs the payload to the backend

## Local dev (no Pi)
1) Create a virtualenv
2) Install requirements
3) Run DRY_RUN=true to test HTTP posting

Example:
DRY_RUN=true BACKEND_INGEST_URL=http://localhost:3000/api/v0/readings python -m hub.src.main
