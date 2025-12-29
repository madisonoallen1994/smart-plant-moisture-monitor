# BLE GATT MVP

This folder contains the **minimal BLE GATT proof-of-concept (MVP)** used during early development to validate Bluetooth Low Energy communication between the plant probe and a central device.

Its purpose is to confirm that:
- BLE advertising works as expected
- A GATT service and characteristic can be defined
- A central (e.g. laptop or hub) can discover, connect, and read data

This folder represents the **earliest BLE experimentation phase** of the project.

---

## What this is

- A lightweight BLE GATT prototype
- Focused on validating BLE mechanics, not full product behavior
- Used to de-risk BLE before building full firmware and hub logic

This code may run on:
- A microcontroller board during early testing
- A temporary test setup separate from the final firmware structure

---

## What this is NOT

- Not the final firmware
- Not production-ready code
- Not optimized for power usage
- Not responsible for sensor accuracy or calibration

Once BLE behavior was validated, this work informed the implementation in `firmware/`.

---

## Why this exists

BLE can be a major source of integration risk.  
This MVP was created to:

- Validate macOS BLE tooling and limitations
- Confirm UUID handling and GATT visibility
- Test reads using tools like nRF Connect
- Establish a known-good BLE contract

By isolating BLE early, later development could proceed with confidence.

---

## Relationship to the rest of the system

- **BLE GATT MVP** (this folder) → early BLE experiments
- **Firmware** (`firmware/`) → full probe firmware informed by this MVP
- **Hub** (`hub/`) → reads BLE data exposed by firmware
- **Backend stub** (`backend_stub/`) → receives readings over HTTP

This folder is primarily historical and reference-oriented.

---

## How to use this folder

You generally do not need to run or modify this code during normal development.

Refer to it if:
- BLE behavior seems unclear or inconsistent
- You want to see the simplest possible GATT setup
- You need a baseline for debugging BLE issues

For active development and hardware day work, use:
- `firmware/` for probe behavior
- `hub/` for BLE reads and forwarding

---

## Future direction

This folder may eventually be:
- Archived
- Converted into reference documentation
- Removed once the firmware is fully stable

For now, it serves as a useful reference point for early BLE decisions.
