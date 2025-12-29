---
notion-url: https://www.notion.so/Product-Specification-2d735ae5cc5080aa8fd4dc53ab910b06
title: Product Specification
date: '2025-12-28 21:26:00.000'
from_notion: https://www.notion.so/Product-Specification-2d735ae5cc5080aa8fd4dc53ab910b06
author: Madison Allen
last_edited_time: '2025-12-29 02:24:00.000'
---
## 1. Product Overview

### What This Product Is

A smart soil moisture monitoring system designed for houseplants.

Each plant is monitored by a low-power, in-soil sensor that measures soil moisture and transmits readings wirelessly to a home hub. The hub forwards readings to a local backend, which evaluates plant health and triggers alerts when watering is needed.

The system allows plant owners to:

- Monitor soil moisture without manual checking

- Receive watering alerts

- Customize thresholds based on plant needs

- Understand plant hydration trends over time

This document defines the **v0 local prototype**, which establishes the full end-to-end system without cloud dependencies.

---

## 2. Why This Product Exists

### User Problems

- Different plants require different watering schedules.

- Manual moisture meters require frequent, active checking.

- Overwatering and underwatering are common and difficult to diagnose.

- Many existing “smart plant” solutions are:

	- Bulky

	- Expensive

	- Closed systems

	- Poorly configurable for different plant types or soil mixes

---

### What This Product Solves

- Passive, always-on soil moisture monitoring

- Plant-specific moisture thresholds

- Automatic alerts when watering is needed

- A modular system that scales from one plant to many

---

## 3. v0 Scope and Constraints

### In Scope (v0)

- One plant

- One soil moisture probe

- One home hub

- One local backend running on a developer machine

- Local alerts and optional mobile app access

### Out of Scope (v0)

- Cloud infrastructure

- Remote access outside the local network

- Push notifications to mobile devices

- Multi-user support

---

## 4. System Architecture (v0)

The system consists of four components:

1. **Plant Probe**

1. **Home Hub**

1. **Local Backend**

1. **Mobile App (optional for v0)**


```plain text
Soil Sensor → BLE Probe → Raspberry Pi Hub → Local Backend → Alerts / App

```

All communication occurs on the **local network**.

---

## 5. Plant Probe

### Purpose

The plant probe continuously measures soil moisture and transmits readings wirelessly while consuming minimal power.

### Hardware (Locked for v0)

- Adafruit Feather nRF52840 Express

- Adafruit STEMMA I²C Capacitive Soil Moisture Sensor

- 3.7V 1200mAh LiPo Battery

- Adafruit Micro-Lipo Charger

- STEMMA JST-PH cabling

---

### Probe Behavior

- The probe wakes on a fixed interval.

- The probe powers the soil sensor and reads a moisture value.

- The probe transmits the reading via Bluetooth Low Energy (BLE).

- The probe returns to deep sleep between readings.

The probe remains battery-powered and physically unobtrusive.

---

## 6. Home Hub

### Purpose

The home hub bridges low-power BLE devices to the local network and backend.

### Hardware (Locked for v0)

- Raspberry Pi Zero W

- 32GB microSD card

- External USB power supply

---

### Hub Behavior

- The hub scans continuously for BLE broadcasts from probes.

- The hub parses moisture readings.

- The hub forwards readings to the local backend over HTTP.

- The hub retries communication when the backend is unavailable.

The hub operates continuously and requires no user interaction during normal operation.

---

## 7. Local Backend (v0)

### Purpose

The local backend acts as the system’s source of truth and alert engine.

### Responsibilities

- Accept moisture readings from the hub

- Store readings locally

- Maintain the latest reading per plant

- Evaluate readings against configured thresholds

- Trigger local alerts when watering is required

### Characteristics

- Runs on a developer machine

- Uses local storage

- Requires no authentication

- Operates entirely on the local network

The backend API shape mirrors a future cloud backend to minimize refactoring later.

---

## 8. Alerts and Notifications (v0)

### Alert Behavior

- Alerts trigger when soil moisture crosses below a configured threshold.

- Alerts trigger only on threshold crossings, not repeated low readings.

- Alerts respect a cooldown period to prevent notification fatigue.

### Alert Delivery (v0)

- Console output

- Optional desktop notifications

Push notifications and remote alerts are deferred to future versions.

---

## 9. Mobile App (Optional for v0)

### Purpose

The mobile app provides visibility into plant moisture levels and alert state.

### v0 Capabilities

- Displays current soil moisture

- Displays last updated timestamp

- Displays plant status (e.g., “OK”, “Needs Water”)

- Allows threshold configuration

The app communicates with the local backend over HTTP and operates on the same network.

---

## 10. Calibration and Thresholds

### Initial Calibration

- Raw moisture values are recorded directly from the sensor.

- Thresholds are configured using raw or normalized values.

### Future Calibration (Planned)

- Plant type–based defaults

- Soil mix–based calibration

- Automated wet/dry calibration flows

---

## 11. Scalability and Future Direction

The v0 architecture supports future expansion to:

- Multiple probes per plant

- Multiple plants per system

- Cloud-based backend

- Remote access and push notifications

- Additional sensors (temperature, light, humidity)

These capabilities are intentionally out of scope for v0 but unblocked by design.

---

## 12. v0 Success Criteria

The prototype is considered successful when:

- Soil moisture readings are stable and accurate

- BLE communication between probe and hub is reliable

- The hub forwards readings to the local backend

- The backend stores data and evaluates thresholds correctly

- Alerts trigger at the appropriate time

- The system operates unattended for multiple days on a local network

