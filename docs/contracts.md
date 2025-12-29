# v0 Data Contract

This document defines the payload format for v0 of the Smart Plant Moisture Monitor system.

## Payload Format

The payload sent from the hub to the backend will include the following fields:

- **`probeId`** (string): Unique identifier for the probe.
- **`timestamp`** (ISO string): The time the reading was generated. For v0, this can be hub-generated.
- **`moistureRaw`** (int): Raw moisture reading from the sensor.
- **`batteryMv`** (int, optional): Battery voltage in millivolts. Optional for v0.
- **`fwVersion`** (string): Firmware version running on the probe.

### Example Payload

```json
{
  "probeId": "probe-001",
  "timestamp": "2025-12-28T12:00:00Z",
  "moistureRaw": 512,
  "batteryMv": 3700,
  "fwVersion": "1.0.0"
}
```
## Transport (v0)
- Probe → Hub uses BLE GATT (Option A).
- Hub reads the latest reading from a GATT characteristic.
- Hub attaches timestamp and POSTs JSON to the backend.

## BLE GATT (Probe → Hub)
- Device name: PlantProbe
- Service UUID: 12345678-1234-1234-1234-1234567890ab
- Characteristic UUID (latestReading): 12345678-1234-1234-1234-1234567890ac
- Characteristic value: UTF-8 JSON string
