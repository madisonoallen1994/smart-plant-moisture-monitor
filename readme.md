# Smart Plant Soil Moisture Monitoring System (v0, Local Prototype)

## What this is
A local-first smart soil moisture monitoring system for houseplants.

Soil Sensor → BLE Plant Probe → Raspberry Pi Hub → Local Backend → Local Alerts / Optional Mobile App

## v0 scope
- 1 plant
- 1 probe
- 1 hub
- 1 local backend (developer machine)
- Optional mobile app on the same local network
- No cloud, no authentication, no remote access

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

## Repo structure
- /firmware  Firmware for the Feather nRF52840 probe
- /hub       Raspberry Pi service that bridges BLE → HTTP
- /backend   Local backend (Node/Express + SQLite recommended)
- /mobile    Optional React Native app (local network only)
- /docs      Contracts, decisions, diagrams, runbooks

## How we work
We only move forward when the current step passes its exit criteria.

## Documentation
All detailed documentation lives in [`/docs`](./docs/readme.md).