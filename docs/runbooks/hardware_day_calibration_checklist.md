# Hardware Day Calibration Checklist (v0)

This checklist defines how to calibrate the capacitive soil moisture sensor
after wiring and basic detection are confirmed.

The goal of v0 calibration is to establish **reference values**, not perfection.

Follow these steps in order.



## Prerequisites

Before starting calibration, confirm:

- [ ] Sensor wiring is complete and correct
- [ ] I²C scanner detects the sensor reliably
- [ ] BLE GATT firmware is running on the probe
- [ ] Hub can read and forward data successfully
- [ ] Soil moisture values are visible in logs

Do not proceed until all prerequisites are met.


## Calibration concepts (read first)

- The sensor reports **raw numeric values**
- Raw values vary by:
  - sensor model
  - soil type
  - probe depth
  - temperature
- Calibration establishes **relative ranges**, not absolute truth

In v0, calibration is **manual and observational**.


## Part 1: Establish “dry” baseline

1. Remove the probe from soil.
2. Wipe the probe clean and dry.
3. Leave the probe exposed to air for 2–3 minutes.
4. Observe the `moistureRaw` value reported by the hub.
5. Record the value as:

- `dry_air_value`

Example:
- `dry_air_value ≈ 800`

Repeat the reading several times to confirm stability.

## Part 2: Establish “dry soil” baseline

1. Insert the probe into **completely dry soil**.
2. Ensure consistent depth (same depth will be used long-term).
3. Wait 2–3 minutes for readings to stabilize.
4. Observe the `moistureRaw` value.
5. Record the value as:

- `dry_soil_value`

Example:
- `dry_soil_value ≈ 650`


## Part 3: Establish “wet soil” baseline

1. Slowly water the soil until it is evenly moist.
2. Do not flood the pot.
3. Wait 3–5 minutes.
4. Observe the `moistureRaw` value.
5. Record the value as:

- `wet_soil_value`

Example:
- `wet_soil_value ≈ 350`


## Part 4: Sanity-check the ranges

Confirm that:

- `dry_air_value` > `dry_soil_value` > `wet_soil_value`
- Values change smoothly over time
- No sudden spikes or drops occur

If this is not true:
- Recheck wiring
- Reinsert the probe
- Repeat measurements


## Part 5: Document calibration values

Record the following in a notes file or README:

- Probe ID
- Plant type
- Soil type
- Pot size
- Probe depth
- `dry_air_value`
- `dry_soil_value`
- `wet_soil_value`

These values are specific to each plant and probe.


## Part 6: Define provisional ranges (v0)

Using the recorded values, define simple ranges:

- Dry: values near `dry_soil_value`
- Okay: values between dry and wet
- Wet: values near `wet_soil_value`

These ranges are **informational only** in v0.

No automation or alerts are triggered.


## Success criteria (stop here)

Calibration is complete when:

- [ ] All three baseline values are recorded
- [ ] Readings are stable and repeatable
- [ ] Value ordering makes sense
- [ ] Notes are documented

At this point, the system is ready for:
- Long-term observation
- Threshold tuning
- Future automation


## Notes

- Calibration may need adjustment over time
- Different plants require different ranges
- Seasonal changes can affect readings

v0 calibration prioritizes learning over precision.
