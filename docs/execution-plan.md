---
notion-url: https://www.notion.so/Execution-Plan-2d735ae5cc50807abee2f87b0257db30
title: Execution Plan
date: '2025-12-28 23:06:00.000'
from_notion: https://www.notion.so/Execution-Plan-2d735ae5cc50807abee2f87b0257db30
author: Madison Allen
last_edited_time: '2025-12-29 02:44:00.000'
---
<br/>

Updated documentation!!!

### Ground rules for this plan

- v0 scope: **1 plant, 1 probe, 1 hub, 1 app**

- You only move forward when the current step passes its **Exit Criteria**

- Keep everything “boring” and observable: logs, timestamps, and simple status screens

---

## Phase 0 — Prep and workspace

### Step 0.1 — Create your repo + folders

**Do**

- Create a single repo (monorepo is easiest for v0):

	- `/firmware`

	- `/hub`

	- `/backend`

	- `/mobile`

	- `/docs`

**Exit criteria**

- Repo exists with those folders and a README that lists the hardware you bought.

### Step 0.2 — Define your v0 data contract (one page)

**Do**

- Decide and write a tiny contract in `/docs/contracts.md`:

Recommended v0 payload (keep it minimal):

- `probeId` (string)

- `timestamp` (ISO string; hub-generated is fine for v0)

- `moistureRaw` (int)

- `batteryMv` (optional for v0)

- `fwVersion` (string)

**Exit criteria**

- A single agreed payload format written down.

---

## Phase 1 — Hardware bring-up (use Hardware Agent Prompt)

### Step 1.1 — Wire the sensor to the Feather via STEMMA QT

**Do**

- Plug the STEMMA soil sensor into the Feather’s STEMMA QT port using the JST-PH cable.

**Exit criteria**

- Physical connection is secure (no loose cable) and power LED behavior looks normal.

### Step 1.2 — Confirm sensor is detectable over I²C

**Do**

- Run an I²C scanner sketch on the Feather (Arduino) to confirm the sensor appears.

- Record the detected I²C address in `/docs/contracts.md`.

**Exit criteria**

- I²C scanner prints the sensor address reliably.

---

## Phase 2 — Probe firmware MVP (use Firmware Agent Prompt)

### Step 2.1 — Firmware: read moisture and print to serial

**Do**

- Implement:

	- Initialize I²C

	- Read moisture value from the STEMMA sensor

	- Print `probeId`, `timestamp`, `moistureRaw` to Serial every 5 seconds (for bench test)

**Exit criteria**

- Serial output shows stable readings that change when you:

	- touch sensor pads / insert into dry soil / insert into wet soil (as applicable)

### Step 2.2 — Firmware: BLE transmit (no sleep yet)

**Do**

- Implement BLE advertising (preferred for v0) that includes the payload.

	- Option A: BLE advertisement manufacturer data (compact)

	- Option B: BLE GATT service with a “latest reading” characteristic (easier to debug)

**Exit criteria**

- Phone app (nRF Connect) sees the probe and can read the moisture value reliably.

### Step 2.3 — Firmware: add low-power behavior (basic)

**Do**

- Add a config constant: `READ_INTERVAL_HOURS` (start with 3 hours later; test with 1 minute now).

- Implement:

	- Wake → read → advertise for N seconds → sleep

- Keep a “debug mode” compile flag to disable sleep during development.

**Exit criteria**

- In test mode (1-minute interval), the probe wakes and broadcasts repeatedly without crashing.

---

## Phase 3 — Hub MVP (use Firmware Prompt for hub behavior + Orchestrator)

### Step 3.1 — Raspberry Pi setup

**Do**

- Flash Raspberry Pi OS Lite to the microSD.

- Enable SSH.

- Connect to Wi-Fi.

- Update packages.

**Exit criteria**

- You can SSH into the Pi reliably.

### Step 3.2 — Hub: BLE scan and log readings locally

**Do**

- Write a small scanner service (Node or Python) that:

	- scans BLE advertisements

	- filters by your `probeId` (or MAC address initially)

	- prints parsed payload to console

	- writes to a local log file with timestamps

**Exit criteria**

- Hub logs each probe reading with timestamp and moisture value.

### Step 3.3 — Hub: forward readings to a dummy endpoint

**Do**

- Stand up a tiny local HTTP endpoint (on your laptop) that prints received JSON.

- Hub POSTs the parsed payload to that endpoint.

**Exit criteria**

- You see payloads arriving end-to-end: probe → hub → endpoint.

---

## Phase 4 — Backend MVP (use Backend Agent Prompt)

### Step 4.1 — Backend: create data models and storage

**Do**

- Implement minimal backend (Firebase suggested for v0):

	- `plants`

	- `probes`

	- `readings`

	- `thresholds` (or threshold on plant)

- Add a simple ingestion endpoint (Cloud Function / Express) that validates payload and stores reading.

**Exit criteria**

- A POST from the hub creates a reading record in the database.

### Step 4.2 — Backend: compute “plant status” and threshold crossing

**Do**

- For v0 (single probe):

	- store threshold on plant (0–100 scaled OR raw value; pick one)

	- compute status:

		- `OK` if above threshold

		- `Needs water` if below threshold

- Add alert rule:

	- triggers only on **above → below** crossing

	- includes a cooldown (default: 24 hours for v0)

**Exit criteria**

- Backend produces an “alert event” when moisture crosses below threshold.

### Step 4.3 — Backend: push notifications (stub then real)

**Do**

- Stub first: log “would send notification”

- Then integrate FCM (and APNs via FCM for iOS) once mobile is ready.

**Exit criteria**

- You can trigger an alert event on demand and see it flow to notification logic.

---

## Phase 5 — Mobile app MVP (use Mobile App Agent Prompt)

### Step 5.1 — Mobile: basic screens with mock data

**Do**

- Build screens:

	- Plant List (single plant card)

	- Plant Detail (moisture value, last updated)

	- Threshold setting (slider or numeric input)

**Exit criteria**

- App runs on device/emulator and screens render cleanly.

### Step 5.2 — Mobile: connect to backend and display live data

**Do**

- Read:

	- latest reading for probe/plant

	- plant threshold

	- plant status

- Show:

	- moisture value

	- last updated timestamp

	- status label

**Exit criteria**

- App updates when new readings arrive (polling is fine for v0).

### Step 5.3 — Mobile: notifications

**Do**

- Add push notification registration + token upload.

- Handle notification open (deep link to Plant Detail).

**Exit criteria**

- You receive a push notification when backend triggers one.

---

## Phase 6 — End-to-end validation (Orchestrator + test checklist)

### Step 6.1 — Real soil test

**Do**

- Place sensor in a plant pot.

- Take baseline readings dry → water plant → observe rising moisture.

**Exit criteria**

- Moisture value changes in the correct direction and remains stable over time.

### Step 6.2 — Threshold + alert validation

**Do**

- Set threshold slightly above current moisture.

- Wait for reading below threshold (or artificially dry sensor).

- Confirm:

	- backend creates alert event

	- push notification arrives

	- app shows “Needs water”

**Exit criteria**

- One alert triggers correctly and does not spam.

### Step 6.3 — Power + sleep validation (short cycle)

**Do**

- Set interval to 5 minutes (temporary).

- Confirm reliable sleep/wake cycles for a few hours.

**Exit criteria**

- No missed wake-ups and hub receives each reading.

---

## Phase 7 — Hardening tasks (still v0, but makes it “real”)

### Step 7.1 — Add offline states

**Do**

- Define “probe offline” as no reading received in 2× interval + grace.

- Show offline state in app and backend.

**Exit criteria**

- Turning off the probe results in offline UI state.

### Step 7.2 — Add battery reporting (optional if easy)

**Do**

- Read LiPo voltage and estimate battery % (rough is okay for v0).

- Include in payload.

- Display in app.

**Exit criteria**

- Battery shows in app and updates occasionally.

---

# How to use your prompts during execution

Use this pattern for each phase:

1. Paste the relevant prompt (Hardware/Firmware/Backend/Mobile)

1. Add: “We are currently on Step X.Y. Produce only what is needed to complete it.”

1. Ask the AI for:

	- implementation notes

	- code skeleton

	- pitfalls

	- a quick validation checklist

---

# Suggested milestones (so this stays fun and not overwhelming)

1. **Milestone 1:** Sensor detected over I²C

1. **Milestone 2:** BLE broadcasts readable in nRF Connect

1. **Milestone 3:** Pi receives and logs readings

1. **Milestone 4:** Backend stores readings

1. **Milestone 5:** App displays live moisture

1. **Milestone 6:** Push notification triggers correctly

1. **Milestone 7:** Probe sleeps/wakes on schedule

---

If you want, I can turn this into a **Notion-ready checklist** (with checkboxes and “exit criteria” fields) or a **Jira epic with stories** for each step.

