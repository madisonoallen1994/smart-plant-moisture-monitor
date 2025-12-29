# Backend Stub (Local Ingest Service)

This folder contains a **minimal local backend service** used during early development and hardware testing of the Smart Plant Moisture Monitoring System.

Its primary purpose is to receive and log sensor readings sent by the hub so the full data flow can be validated **without** needing a real backend or cloud infrastructure.


## What this is

- A small FastAPI application
- Listens on `http://localhost:3000`
- Accepts HTTP `POST` requests from the hub at `/api/v0/readings`
- Prints received payloads to the console
- Returns `200 OK` for successful ingest

This is intentionally simple and local-only.


## What this is NOT

- Not a production backend
- Not a database
- Not deployed anywhere
- Not responsible for data persistence, auth, or analytics

It exists purely to unblock hub + hardware development.


## When to use this

Use the backend stub when:
- Running the hub in `DRY_RUN=true`
- Testing BLE → hub → backend flow
- Validating payload structure and timing
- Debugging hardware day issues without adding backend complexity


## How to run

From the repository root:
```bash
cd backend_stub
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```
You should see output indicating the server is running on port 3000.


## Health check

To confirm the service is running:
```bash
    curl http://localhost:3000/health
```
Expected response:
```json 
    {"ok": true, "ts": "..."}
```

## Injest endpoint

- The hub sends readings to: `POST /api/v0/readings` 
- Example reading: 
```json
{
  "probeId": "probe-001",
  "timestamp": "2025-12-29T17:22:41Z",
  "moistureRaw": 500,
  "fwVersion": "0.1.0",
  "batteryMv": 3700,
  "rssi": -62
}
```
- When a payload is received, it will be printed to the console.

## Relationship to the rest of the system

- Firmware → sends raw sensor data over BLE
- Hub → reads BLE data and forwards it via HTTP
- Backend stub (this) → receives and logs the data
This allows end-to-end testing without a real backend.


## Future direction

This folder may eventually be:
- Replaced by a real backend service
- Extended to write data to disk
- Used for local replay/testing tools
For now, it stays intentionally minimal.
