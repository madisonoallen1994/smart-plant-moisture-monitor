# Architecture Overview (v0)

This document describes the v0 system architecture for the Smart Plant Soil Moisture Monitoring System.

The goal of v0 is to validate the full local data path: `PlantProbe → Home Hub → Local Backend`

## Components

### 1) PlantProbe (device)

- Hardware: Adafruit Feather nRF52 + capacitive soil moisture sensor (I²C)
- Role: reads raw soil moisture data and exposes it over BLE
- Communication: BLE GATT peripheral

v0 BLE identity:

- Device name: `PlantProbe`
- Service UUID: `12345678-1234-1234-1234-1234567890ab`
- Characteristic UUID (latest reading): `12345678-1234-1234-1234-1234567890ac`
- Characteristic value format: UTF-8 encoded JSON string

### 2) Home Hub (local computer or Raspberry Pi)

- Role: BLE Central that polls the probe and forwards readings
- Language: Python
- Key libraries: `bleak`, `requests`
- Runs locally (no cloud dependency in v0)

v0 hub behavior:

- Identifies the probe by BLE address (preferred) or device name
- Connects to the probe
- Reads the GATT characteristic
- Disconnects immediately after reading
- Repeats this process on a fixed poll interval
- Adds a UTC timestamp before forwarding data

### 3) Local Backend (v0)

- Role: receives readings and stores or displays them locally
- Communication: HTTP from Hub to Backend
- v0 state: simple local receiver used for validation
- Future versions may add persistence and query endpoints


## Data Flow (v0)

This section describes how data moves through the system during normal operation.

### High-level flow

1. The PlantProbe reads raw soil moisture data from the sensor over I²C.
2. The PlantProbe packages the reading into a small JSON payload.
3. The PlantProbe exposes the payload via a BLE GATT characteristic.
4. The Home Hub connects to the PlantProbe over BLE.
5. The Home Hub reads the GATT characteristic.
6. The Home Hub adds a UTC timestamp to the reading.
7. The Home Hub sends the reading to the local backend via HTTP.


### Detailed step-by-step flow

#### Step 1: Sensor read (PlantProbe)

- The soil moisture sensor is read over I²C.
- The raw value is not calibrated in v0.
- Example raw value: `500`

#### Step 2: Payload creation (PlantProbe)

- The PlantProbe builds a JSON object with:
  - `probeId`
  - `moistureRaw`
  - `fwVersion`
- This payload represents the *latest* reading only.
- Example (conceptual): `{"probeId":"probe-001","moistureRaw":500,"fwVersion":"0.1.0"}`

#### Step 3: BLE exposure (PlantProbe → Hub)

- The JSON payload is exposed via:
  - One BLE service
  - One BLE characteristic
- The characteristic value is a UTF-8 encoded string.
- The probe advertises continuously while powered.

#### Step 4: BLE polling (Home Hub)

- The Home Hub:
  - Identifies the probe by BLE address or device name
  - Connects to the probe
  - Reads the characteristic once
  - Disconnects immediately
- No BLE connection is held between poll cycles.

#### Step 5: Timestamp injection (Home Hub)

- The Home Hub adds:
  - `timestamp` (UTC, ISO-8601 format)
- This ensures consistent timing regardless of device clock drift.

#### Step 6: Backend POST (Home Hub → Backend)

- The Home Hub sends an HTTP POST request to the backend.
- The payload includes:
  - `probeId`
  - `timestamp`
  - `moistureRaw`
  - `fwVersion`
- Example (conceptual): `{"probeId":"probe-001","timestamp":"2025-12-29T03:16:29Z","moistureRaw":500,"fwVersion":"0.1.0"}`


### Polling behavior

- Polling runs on a fixed interval (v0 default: 10 seconds).
- Each poll cycle is independent.
- Failures do not stop future cycles.


### Failure handling (v0)

- BLE read failures:
  - Are logged
  - Do not crash the hub
- Backend POST failures:
  - Are logged
  - Do not crash the hub
- The next poll cycle proceeds as normal.


### v0 assumptions and constraints

- Only one probe is supported.
- Only the latest reading is exposed.
- No buffering or retry queue exists.
- Data loss is acceptable during development.

These constraints are intentional for v0.


## Interfaces and Contracts (v0)

This section defines the explicit interfaces between system components in v0.
These contracts are intentionally small and stable.


### Probe → Hub (BLE GATT)

The PlantProbe exposes the latest sensor reading via BLE GATT.

#### Discovery

- Device name: `PlantProbe`
- The hub may identify the probe by:
  - Explicit BLE address (preferred), or
  - Device name (fallback)

#### BLE Service

- Service UUID: `12345678-1234-1234-1234-1234567890ab`

This service represents the PlantProbe data service.

#### BLE Characteristic

- Characteristic UUID: `12345678-1234-1234-1234-1234567890ac`
- Purpose: expose the latest sensor reading
- Access: read (notify optional)
- Encoding: UTF-8 string

#### Characteristic payload (v0)

The characteristic value is a UTF-8 encoded JSON object with the following fields:

- `probeId` (string)
  - Unique identifier for the probe
- `moistureRaw` (number)
  - Raw, uncalibrated sensor reading
- `fwVersion` (string)
  - Firmware version running on the probe

Example payload: `{"probeId":"probe-001","moistureRaw":500,"fwVersion":"0.1.0"}`

Notes:
- Only the latest reading is exposed
- No timestamp is included at the probe level in v0


### Hub → Backend (HTTP)

The Home Hub forwards readings to the backend using HTTP.

#### Endpoint

- Method: `POST`
- Path: `/api/v0/readings`
- Transport: HTTP (local development)

#### Request payload

The hub sends a JSON payload with the following fields:

- `probeId` (string)
- `timestamp` (string, ISO-8601, UTC)
- `moistureRaw` (number)
- `fwVersion` (string)

Example payload:

- `{"probeId":"probe-001","timestamp":"2025-12-29T03:16:29Z","moistureRaw":500,"fwVersion":"0.1.0"}`

#### Hub responsibilities

- Generate the `timestamp`
- Ensure the payload matches the v0 data contract
- Log failures without crashing


### Contract stability (v0)

The following are considered stable for v0:

- BLE service UUID
- BLE characteristic UUID
- JSON field names
- Field data types

Any changes to these require a new contract version.


### Explicit exclusions (v0)

The following are intentionally not part of the v0 contract:

- Calibration data
- Moisture thresholds or status labels
- Battery voltage reporting
- Multiple probes per hub
- Authentication or encryption

These may be added in future versions once v0 is validated.


## Runtime Behavior (v0)

This section describes how the system behaves while running under normal and error conditions.


### Hub startup

When the Home Hub starts:

- Configuration is loaded from environment variables.
- The hub logs its startup mode (`dry_run` or `ble`).
- The polling loop is initialized.
- No BLE connection is attempted until the first poll cycle begins.


### Poll cycle lifecycle

Each poll cycle follows the same sequence:

1. Start of poll cycle is logged.
2. The hub determines operating mode:
   - `dry_run` mode: skip BLE and generate a fake reading.
   - `ble` mode: attempt BLE connection to the probe.
3. If in BLE mode:
   - Connect to the PlantProbe.
   - Read the GATT characteristic once.
   - Disconnect immediately.
4. Parse the reading payload.
5. Add a UTC timestamp.
6. Attempt to POST the payload to the backend.
7. Log success or failure.
8. Sleep until the next poll interval.

Each poll cycle is independent of previous cycles.


### Timing behavior

- Polling occurs on a fixed interval (v0 default: 10 seconds).
- Poll timing does not drift based on execution time.
- Slow or failed operations do not block future cycles.


### BLE connection behavior

- The hub does not maintain a persistent BLE connection.
- A fresh BLE connection is created for each poll cycle.
- BLE connections are short-lived by design to:
  - Reduce coupling
  - Avoid stale connections
  - Simplify failure recovery


### Failure handling

#### BLE failures

If a BLE operation fails:

- The failure is logged with context.
- The current poll cycle ends.
- The hub does not crash.
- The next poll cycle proceeds as scheduled.

#### Backend failures

If the backend POST fails:

- The failure is logged.
- No retry is attempted in v0.
- The hub continues polling on the next cycle.


### Logging behavior

- All major lifecycle events are logged.
- Logs include:
  - Startup mode
  - Poll cycle start and end
  - BLE read success or failure
  - Backend POST success or failure
- Logging is intended for debugging and validation in v0.


### Shutdown behavior

- The hub can be stopped safely using standard process termination (Ctrl+C).
- No cleanup is required between runs.
- Restarting the hub resumes polling normally.


### v0 design assumptions

- Temporary data loss is acceptable.
- Real-time guarantees are not required.
- Observability via logs is sufficient.
- Simplicity and debuggability are prioritized over optimization.

These assumptions may change in future versions.


## Non-goals and Out of Scope (v0)

This section lists features and concerns that are intentionally excluded from v0.
Excluding these keeps the initial system simple, testable, and easy to debug.


### Cloud infrastructure

- No cloud deployment
- No hosted backend
- No remote access
- No multi-user support

v0 runs entirely on local hardware.


### Multiple probes

- Only one PlantProbe is supported
- No probe discovery orchestration
- No scheduling across multiple devices

Multi-probe support will be addressed in a future version.


### Power optimization

- No deep sleep or low-power modes
- No battery life optimization
- No power state reporting

v0 prioritizes correctness over efficiency.


### Sensor calibration and interpretation

- No calibration curves
- No conversion from raw values to percentages
- No plant-specific thresholds
- No “dry / okay / wet” labels

Raw sensor values are passed through unchanged.


### Data durability and retries

- No buffering of failed readings
- No retry queue for backend failures
- No local persistence of readings

Temporary data loss is acceptable in v0.


### Alerts and automation

- No alerts or notifications
- No automatic watering
- No rule engine

v0 is observational only.


### Security and authentication

- No authentication
- No encryption beyond default BLE transport
- No access control

Security will be addressed after functional validation.


### UI and visualization

- No dashboard
- No charts or graphs
- No mobile or web UI

Data inspection is done via logs and local tools only.


### Summary

v0 exists to prove that:

- The hardware can read soil moisture reliably
- BLE communication is stable
- The hub can poll and forward data continuously
- The system is debuggable and understandable

Once these are validated, future versions can safely expand scope.


---

## Diagram (Mermaid)

```mermaid
flowchart LR
  %% v0 data path: PlantProbe -> Home Hub -> Local Backend

  subgraph Probe["PlantProbe (device)"]
    Sensor["Capacitive Soil Moisture Sensor (I²C)"]
    FW["Firmware (Feather nRF52)\n- reads sensor\n- exposes GATT"]
    Sensor -->|I²C| FW
  end

  subgraph BLE["BLE GATT (Probe → Hub)"]
    Adv["Advertises as: PlantProbe"]
    Svc["Service UUID\n12345678-1234-1234-1234-1234567890ab"]
    Char["Characteristic: latestReading\nUUID 12345678-1234-1234-1234-1234567890ac\nValue: UTF-8 JSON string"]
    Adv --> Svc --> Char
  end

  subgraph Hub["Home Hub (local)"]
    HubSvc["Python Hub Service\n(bleak + requests)"]
    Poll["Poll loop\nconnect → read → disconnect\nrepeat every N seconds"]
    HubSvc --> Poll
  end

  subgraph Backend["Local Backend (v0)"]
    API["HTTP ingest\nPOST /api/v0/readings"]
    Store["Storage/logging (v0)"]
    API --> Store
  end

  FW -->|Expose GATT service| BLE
  Poll -->|Read latestReading| Char
  Poll -->|POST JSON payload| API
