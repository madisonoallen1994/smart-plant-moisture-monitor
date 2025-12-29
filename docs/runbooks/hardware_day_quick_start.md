# Hardware Day Quick Start (v0)

This is the fastest path from “hardware arrived” to “end-to-end data flow working.”

Use this when you want to move quickly without hunting through multiple docs.


## What you need

- Laptop with this repo pulled and up to date
- Arduino IDE installed
- nRF Connect installed on phone
- Adafruit Feather nRF52 + sensor wired (see wiring runbook)


## Repo + branch

Open terminal at repo root.

Confirm you are on the hardware branch:

    git branch

Expected: the active branch has a `*` next to `hardware-day`.

If not:

    git checkout hardware-day
    git pull


## Flash the firmware (Probe)

Open Arduino IDE.

Open the firmware sketch:

- `firmware/ble_gatt_mvp/ble_gatt_mvp.ino`

Set Arduino IDE options:

- Tools → Board → `Adafruit Feather nRF52840 Express`
- Tools → Port → select the Feather port

Upload firmware (Arduino “Upload” button).

Confirm firmware is running (Serial Monitor):

- Baud: `115200`
- Look for:
  - `BLE GATT MVP starting...`
  - `Advertising started.`


## Verify BLE on phone (nRF Connect)

Open nRF Connect.

Scan and connect to:

- Device name: `PlantProbe`

Confirm service and characteristic:

- Service UUID: `12345678-1234-1234-1234-1234567890ab`
- Characteristic UUID: `12345678-1234-1234-1234-1234567890ac`

Read the characteristic.

Expected: a JSON string containing `probeId`, `moistureRaw`, `fwVersion`.

Record the BLE address shown in nRF Connect:

- `AA:BB:CC:DD:EE:FF`


## Confirm sensor direction (required)

Follow the “Direction Confirmation Checklist”:

- `docs/runbooks/hardware_day_calibration_checklist.md`

Record:

- `air_raw`
- `dry_soil_raw`
- `wet_soil_raw`
- Sensor direction: `wet = higher` OR `wet = lower`

Do not set thresholds until direction is confirmed.


## Configure the hub (local)

Open `hub/.env` and set:

- `DRY_RUN=false`
- `PROBE_ADDRESS=AA:BB:CC:DD:EE:FF` (use the real address)

Do not change UUID values.


## Run the hub

From repo root:

    source hub/.venv/bin/activate
    set -a; source hub/.env; set +a
    python -m hub.src.main

Expected logs:

- Hub starts
- BLE read succeeds
- A payload is logged
- The hub posts to the backend endpoint
- Polling repeats every 10 seconds


## If you see “connection refused” when posting

This means the backend is not running locally.

Start the local backend stub (if present), or follow the backend setup steps.


## Done criteria

You are done when:

- PlantProbe appears in nRF Connect
- Characteristic read returns JSON
- Hub reads BLE successfully
- Hub runs multiple poll cycles without crashing
- Hub can POST readings to a local endpoint without errors


## Where to go next

- Sensor wiring: `docs/runbooks/hardware_day_sensor_wiring.md`
- Calibration: `docs/runbooks/hardware_day_calibration_checklist.md`
- Normal readings: `docs/normal_readings_reference.md`
- Architecture: `docs/architecture_v0.md`
