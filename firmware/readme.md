# Firmware (Plant Probe)

This folder contains the **firmware that runs on the physical plant probe** hardware.

The firmware is responsible for:
- Reading raw soil moisture sensor values
- Advertising the device over Bluetooth Low Energy (BLE)
- Exposing sensor readings via a BLE GATT service and characteristic

It is the lowest-level component in the system and runs directly on the microcontroller.


## What this is

- Embedded firmware for the plant probe
- Runs on a microcontroller board
- Interfaces directly with the soil moisture sensor
- Publishes data over BLE for the hub to consume

The firmware does not know anything about backends, HTTP, or data storage.


## What this is NOT

- Not a Python service
- Not a backend
- Not responsible for networking beyond BLE
- Not responsible for timestamps, retries, or data forwarding

Those concerns live in the hub.


## Responsibilities

The firmware is responsible for:

- Initializing the soil moisture sensor
- Periodically sampling raw moisture values
- Starting BLE advertising
- Defining a BLE GATT service
- Updating a readable characteristic with the latest sensor value

The hub connects as a BLE central and reads from this characteristic.


## BLE contract

The firmware defines the BLE contract that the hub relies on.

This includes:
- A **service UUID**
- A **characteristic UUID**
- Characteristic permissions (read, and optionally notify)
- Payload format (raw integer value or encoded bytes)

These UUIDs must match the values configured in the hub’s `.env` file.


## Relationship to the rest of the system

- **Firmware** (this folder) runs on the probe hardware
- **Hub** (`hub/`) connects over BLE and reads data
- **Backend stub** (`backend_stub/`) receives readings over HTTP during development
- **Future backend** will eventually persist and analyze the data

Each layer is intentionally decoupled.


## Development notes

- Firmware is typically flashed via USB during development
- BLE behavior can be inspected using tools like nRF Connect
- Changes to BLE services or characteristics require corresponding updates in the hub configuration

Hardware-day troubleshooting steps related to BLE are documented in:
`docs/runbooks/hardware_day_quick_start.md`


## Future direction

The firmware may eventually:
- Support additional sensors (temperature, battery level)
- Support BLE notifications instead of polling
- Implement power-saving sleep modes
- Add basic calibration or filtering

For now, it is focused on reliability and clarity during early prototyping.
