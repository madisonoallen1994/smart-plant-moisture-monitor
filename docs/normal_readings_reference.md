# Normal Moisture Readings Reference (v0)

This document explains how to interpret `moistureRaw` values during normal use.

It is meant to answer the question:
“Is this reading normal, and should I be concerned?”

This guide assumes calibration has already been completed.


## Important context (read first)

- `moistureRaw` values are **relative**, not absolute
- Numbers vary by:
  - sensor
  - soil type
  - probe depth
  - pot size
  - temperature
- There is no universal “correct” number

Normal readings are defined **relative to your calibrated baselines**.


## Typical value ordering

After calibration, values should generally follow this pattern:

- Highest values → dry air
- Mid-range values → dry soil
- Lowest values → wet soil

Example (illustrative only):

- Dry air: ~800
- Dry soil: ~650
- Wet soil: ~350

Your numbers will differ — the ordering matters more than the exact values.


## What normal behavior looks like

### Immediately after watering

- `moistureRaw` drops noticeably
- Values may continue dropping for several minutes
- Readings stabilize after soil absorbs water

This is expected behavior.


### Several hours after watering

- Values remain relatively stable
- Small fluctuations (±10–30) are normal
- No sharp jumps should occur


### Over multiple days (no watering)

- `moistureRaw` increases gradually
- Change is slow and monotonic
- Sudden jumps are unusual

A slow upward trend indicates drying soil.


## Expected daily patterns

Normal patterns include:

- Slight dips after watering
- Gradual rise as soil dries
- Minor noise between readings

Abnormal patterns include:

- Large jumps up or down between readings
- Rapid oscillation
- Values that do not change at all over long periods


## What readings usually mean

### Readings near “wet soil” baseline

- Soil is moist
- No action needed
- Overwatering risk if values stay here continuously


### Readings between wet and dry soil

- Ideal range for most plants
- Normal daily variation expected
- No concern


### Readings near “dry soil” baseline

- Soil is drying
- Plant may need water soon
- Timing depends on plant type


### Readings higher than dry soil baseline

- Soil is very dry
- Plant likely needs watering
- Prolonged time here may stress the plant


## Common anomalies and interpretations

### Sudden spike upward

Possible causes:

- Probe partially pulled out of soil
- Loose wiring
- Soil shifting around probe

Action:
- Check probe placement
- Reseat probe if needed


### Sudden drop downward

Possible causes:

- Recent watering
- Water pooling near probe
- Accidental contact with water

Action:
- Wait for stabilization
- Confirm soil moisture distribution


### Flat readings over long periods

Possible causes:

- Sensor not updating
- Firmware not reading sensor
- Probe disconnected

Action:
- Verify I²C readings
- Check wiring and firmware logs


## How often to worry

Do not worry about:

- Small fluctuations
- One-off spikes that self-correct
- Minor differences day to day

Investigate if:

- Readings stop changing entirely
- Large jumps repeat consistently
- Values contradict visible soil conditions


## v0 usage guidance

In v0, readings are for:

- Observation
- Learning plant behavior
- Understanding drying patterns

They are not yet used for:

- Alerts
- Automation
- Watering decisions

Those come later.


## Summary

Normal readings are:

- Consistent
- Gradual
- Predictable relative to calibration

Unexpected readings are usually caused by:
- Physical probe issues
- Soil movement
- Recent watering events

Use trends, not single values, to judge plant health.


## Notes

- Each plant will behave differently
- Seasonal changes affect readings
- Recalibration may be needed over time

This document is a reference, not a rulebook.
