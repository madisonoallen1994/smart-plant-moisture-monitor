# Smart Plant Soil Moisture Monitoring System (v0, Local Prototype)
This repository contains the code and documentation for a local-first, BLE-based smart soil moisture monitoring system for houseplants.

The system is designed to:
- Read raw soil moisture data from a physical probe
- Transmit readings over Bluetooth Low Energy (BLE)
- Forward data through a local hub to a backend service
- Support rapid prototyping, hardware testing, and iteration

The project is intentionally modular so hardware, software, and backend work can evolve independently.


## What this is
A local-first smart soil moisture monitoring system for houseplants.

High-level flow: 
```python
Soil Sensor
    ↓
BLE Plant Probe
    ↓
Hub (Laptop or Raspberry Pi)
    ↓
Local Backend
    ↓
Local Alerts / Optional Mobile App
```

## v0 scope
This repository represents version 0 (local prototype) of the system.
v0 is intentionally constrained:
- 1 plant
- 1 probe
- 1 hub
- 1 local backend (developer machine)
- Optional mobile app on the same local network
- No cloud
- No authentication
- No remote access
The goal of v0 is to prove hardware reliability and end-to-end data flow, not scale.

## Locked hardware (v0)

### Plant Probe
- Adafruit Feather nRF52840 Express
- Adafruit STEMMA I²C Capacitive Soil Moisture Sensor
- 3.7V 1200mAh LiPo Battery
- Adafruit Micro-Lipo Charger
- STEMMA JST-PH cabling

### Home Hub
- Raspberry Pi Zero W
- 32GB microSD card
- External 5V micro-USB power supply
During development, the hub may also run on a laptop.

## High-level architecture 
```java 
Plant Probe (Firmware)
        ↓ BLE
      Hub (Python)
        ↓ HTTP
  Backend Stub (Local)
```
- The probe measures soil moisture and exposes readings over BLE
- The hub reads BLE data and forwards it over HTTP
- The backend receives and logs readings locally

## Repo structure
```pgsql
.
├── firmware/          Firmware that runs on the physical probe
│   ├── sketches/      Exploratory and experimental sketches
│   └── ble_gatt_mvp/  Early BLE GATT proof-of-concept
├── hub/               Local BLE reader and HTTP forwarder
│   ├── src/           Hub source code
│   └── logs/          Runtime logs (not committed)
├── backend_stub/      Minimal local backend ingest service
├── mobile/            Optional local-network mobile app
├── docs/              Project documentation
│   ├── runbooks/      Setup and troubleshooting guides
│   ├── decisions/     Architecture and design decisions
│   └── diagrams/      System and data flow diagrams
└── README.md          This file
```
Each major folder contains its own README explaining its purpose.

## Key components 

### Firmware
Runs on the physical plant probe and is responsible for:
- Reading raw soil moisture values
- Advertising over BLE
- Exposing data via a BLE GATT service and characteristic
See: firmware/README.md

--- 

### Hub 
A Python service that:
- Scans for the probe over BLE
- Reads sensor data from a GATT characteristic
- Forwards readings to a backend over HTTP
- Supports a DRY_RUN mode for testing without hardware
See: hub/README.md

---

### Backend stub
A minimal local HTTP service used during development to:
- Receive readings from the hub
- Log payloads to the console
- Validate end-to-end data flow without a real backend
See: backend_stub/README.md


## How we work
We move forward one step at a time.

Each phase has explicit exit criteria, and we do not advance until:
- The current step works reliably
- The data flow is validated end-to-end
- The system can be debugged easily if something breaks
This keeps hardware development predictable and low-stress.

## Documentation
All detailed documentation lives in the docs folder.

Start here if you are new to the project:
- docs/README.md
- docs/runbooks/hardware_day_quick_start.md

Documentation includes:
- System and product specifications
- Architecture and design decisions
- Diagrams and data flow visuals
- Hands-on runbooks for setup and troubleshooting

## Project status 
This project is currently in v0 local prototype / hardware-day development.

Priorities at this stage:
- Reliability over optimization
- Clear separation of responsibilities
- Strong documentation and debuggability
Production deployment, persistence, and cloud infrastructure are intentionally out of scope.

## Future direction

Possible future enhancements include:
- Running the hub exclusively on a Raspberry Pi
- Supporting multiple probes
- Adding calibration and normalization
- Replacing the local backend stub with a real backend
- Optional remote access or cloud sync
These will be considered only after v0 is stable.

## Getting started

If you are coming in fresh:
- Read docs/README.md
- Follow docs/runbooks/hardware_day_quick_start.md
- Refer to individual folder READMEs as needed
This repository is designed to be approachable even without prior context.