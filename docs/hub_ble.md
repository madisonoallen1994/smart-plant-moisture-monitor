# Hub BLE Behavior (v0)

This document defines the v0 BLE Central behavior for the Hub when communicating with PlantProbe devices.

The goal of v0 is to provide a simple, reliable, and debuggable BLE integration that minimizes connection complexity and failure modes.

---

## Identity and Discovery

- The hub identifies a probe using `PROBE_ADDRESS` when it is provided.
- The hub uses `PROBE_NAME` only when `PROBE_ADDRESS` is not provided.
- When using name-based discovery, the hub scans for up to **8 seconds** per attempt.
- When a probe is discovered, the hub logs the resolved BLE address.

---

## Connection Strategy

- The hub uses a **connect → read → disconnect** pattern.
- The hub does not maintain a long-lived BLE connection in v0.
- The hub connects to **one probe at a time**.
- The hub does not attempt parallel BLE connections in v0.

---

## Read Strategy

- The hub reads the `latestReading` GATT characteristic once per poll cycle.
- The characteristic UUID is defined by `CHAR_UUID`.
- The characteristic value is treated as a **UTF-8 encoded JSON string**.
- The hub rejects a reading if the value cannot be parsed as a JSON object.

---

## Poll Cadence

- The hub waits `POLL_INTERVAL_SECONDS` between poll cycles.
- The next poll cycle begins even if the previous poll failed.
- Poll cycles are independent and idempotent.

---

## Retry Behavior

- If scanning fails, the hub retries during the next poll cycle.
- If connecting fails, the hub retries during the next poll cycle.
- If reading fails, the hub retries during the next poll cycle.
- The hub does not implement exponential backoff in v0.

---

## Logging

- The hub logs one entry per poll cycle.
- Each poll log includes:
  - probe address
  - characteristic UUID
  - success or failure status
- On success, the hub logs the parsed JSON payload.
- On failure, the hub logs the exception message.

---

## Timestamp Behavior

- The hub generates a `timestamp` in UTC.
- The timestamp uses ISO-8601 format.
- The timestamp is attached only when sending data to the backend.

---

## Failure Handling

- A BLE failure does not crash the hub process.
- A backend POST failure does not crash the hub process.
- The hub continues running until manually stopped.

---

## v0 Design Rationale

This behavior prioritizes:
- predictable BLE behavior
- low operational complexity
- clear logging and debuggability
- easy iteration for future versions

More advanced features such as notification subscriptions, parallel connections, and exponential backoff are intentionally deferred to later versions.
