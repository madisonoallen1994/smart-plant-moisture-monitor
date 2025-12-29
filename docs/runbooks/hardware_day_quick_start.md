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

## macOS BLE Troubleshooting Checklist

### 1. Board not showing up as a serial device

Symptoms
- Board does not appear in Arduino IDE or CircuitPython.
- No `/dev/cu.usb*` or `/dev/tty.usb*` devices appear.
- Board may only appear as a serial device when in bootloader or flashing mode.

Checks
- Use a data-capable USB cable (not charge-only).
- Try a different USB port (avoid hubs if possible).
- Reboot the board while plugged in.
- Restart the Arduino IDE or serial monitor.

macOS check
```bash
ls /dev/cu.*
```

If still missing
- Restart macOS Bluetooth.
- Reboot the laptop if the USB stack is wedged.

---

### 2. Device not advertising over BLE

Symptoms
- Probe does not appear in BLE scans
- Hub cannot discover the device during scan

Checks
- Open nRF Connect (mobile) and scan for devices
- Confirm firmware explicitly starts advertising
- Ensure the board is powered (battery vs USB matters)

nRF Connect tips
- Pull down to refresh the scan
- Toggle Bluetooth off/on inside the app
- Note the MAC address once discovered

Action
- Copy the MAC address into `.env`
```env
PROBE_ADDRESS=AA:BB:CC:DD:EE:FF
```
- Note: filtering by address is more reliable than name filtering on macOS.

---

### 3. Device connects but characteristics cannot be read

Symptoms
- Probe appears in BLE scan and connects successfully
- Hub connects but fails when reading the characteristic
- Errors such as “characteristic not found” or read timeouts

Checks
- Confirm the service UUID matches `SERVICE_UUID` in `.env`
- Confirm the characteristic UUID matches `CHAR_UUID` in `.env`
- Verify the firmware exposes the characteristic with read permissions
- Ensure the device is not already connected to another central (e.g. nRF Connect)

nRF Connect checks
- Connect to the device
- Expand the service list
- Manually locate the expected service and characteristic
- Attempt a manual read in nRF Connect

Action
- Update UUIDs in `.env` to exactly match what is shown in nRF Connect
```env
SERVICE_UUID=12345678-1234-1234-1234-1234567890ab
CHAR_UUID=12345678-1234-1234-1234-1234567890ac
```

Notes
- UUIDs are case-insensitive but must be an exact match
- macOS may cache stale GATT data; power-cycle the board if changes were made

### 4. Device connects but returns invalid or empty data

Symptoms
- Hub connects and reads the characteristic
- Returned values are empty, zero, or clearly incorrect
- Payload is missing expected fields

Checks
- Confirm the firmware is writing data to the characteristic before reads occur
- Verify the characteristic value is updated on each poll cycle
- Check that the firmware and hub agree on payload encoding (raw bytes vs JSON)
- Confirm the characteristic supports read (and notify, if used)

nRF Connect checks
- Read the characteristic manually in nRF Connect
- Observe whether values change between reads
- Verify the raw byte length matches expectations

Action
- Log raw characteristic bytes in the hub before decoding
- Compare raw values against known good reference payloads

Notes
- macOS BLE may return cached values if the device is not updating the characteristic
- Power-cycling the device can clear stale state

--- 

### 5. Bluetooth permissions or system issues on macOS

Symptoms
- BLE scans return no devices
- Connections fail intermittently
- Behavior changes after sleep, reboot, or OS update

Checks
- Confirm Bluetooth is enabled in macOS system settings
- Ensure Terminal has Bluetooth permissions
- Ensure any Python IDE (VS Code, PyCharm) has Bluetooth permissions

macOS permissions
- System Settings → Privacy & Security → Bluetooth
- Enable Bluetooth access for:
  - Terminal
  - VS Code (if running the hub from VS Code)

Action
- Restart Bluetooth from the menu bar
- Toggle Bluetooth off and back on
- Restart the hub after permissions changes

Advanced recovery
- Fully power off the Mac (not sleep)
- Wait 30 seconds before rebooting
- Reconnect and retry BLE scan


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


