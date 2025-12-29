# Hardware Day BLE Checklist (v0)

This checklist walks through validating PlantProbe end-to-end:
power → BLE verification → hub reads BLE → hub POSTs payload.

Follow these steps in order. Do not skip steps.

## Part 1: Prepare the computer

- [ ] Open this repo in VS Code
- [ ] Open a terminal at the repo root
- [ ] Confirm Arduino IDE opens successfully
- [ ] Confirm nRF Connect is installed on a phone (iOS or Android)

## Part 2: Flash the PlantProbe firmware (Feather)

1. Plug the Adafruit Feather nRF52 into the computer using USB.
2. Open Arduino IDE.
3. Open the sketch file: `firmware/ble_gatt_mvp/ble_gatt_mvp.ino`
4. In Arduino IDE:
   - Tools → Board → `Adafruit Feather nRF52840 Express`
   - Tools → Port → select the Feather’s port
5. Click Upload.
6. Wait for upload to finish successfully.

Confirm firmware is running:
- Open Serial Monitor
- Set baud rate to `115200`
- You should see:
  - `BLE GATT MVP starting...`
  - `Advertising started.`

If you do not see this:
- Re-upload the sketch
- Confirm the correct board and port are selected

## Part 3: Verify BLE using nRF Connect (phone)

1. Open nRF Connect on the phone.
2. Tap Scan.
3. Look for a device named `PlantProbe`.
4. Tap Connect.

Verify the GATT service:
- Find Service UUID: `12345678-1234-1234-1234-1234567890ab`

Verify the characteristic:
- Find Characteristic UUID: `12345678-1234-1234-1234-1234567890ac`
- Tap Read

Expected value:
- A UTF-8 JSON string similar to:
  `{"probeId":"probe-001","moistureRaw":500,"fwVersion":"0.1.0"}`

Optional:
- Enable Notify
- You should see updates every ~5 seconds

## Part 4: Capture the BLE address (important)

In nRF Connect, note the BLE address for `PlantProbe`. It looks like `AA:BB:CC:DD:EE:FF`.

Write it down. The hub will use this address.

## Part 5: Configure the hub (laptop)

1. Open `hub/.env`
2. Update:

`DRY_RUN=false`  
`PROBE_ADDRESS=AA:BB:CC:DD:EE:FF`

Replace the address with the real one from nRF Connect.

Do not change the UUIDs.

## Part 6: Run the hub

In the terminal, run the following commands:

    source hub/.venv/bin/activate
    set -a; source hub/.env; set +a
    python -m hub.src.main

Expected behavior:

- Logs show `Poll cycle start mode=ble`
- Logs show BLE read success
- Logs show a POST payload
- The hub continues polling every 10 seconds

If errors occur:

- Confirm PlantProbe is powered and still advertising
- Confirm the BLE address is correct
- Confirm nRF Connect can still read the characteristic

## Part 7: Success Criteria (stop here)

You are done when:
1. PlantProbe appears in nRF Connect
2. Characteristic read returns a JSON string
3. Hub can read BLE successfully
4. Hub keeps polling without crashing

Notes:
- Moisture value is stubbed (500) in v0
- Real sensor readings will be added after wiring the soil moisture sensor