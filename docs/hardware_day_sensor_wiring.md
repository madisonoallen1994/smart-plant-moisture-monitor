# Hardware Day Sensor Wiring Checklist (v0)

This checklist covers wiring the capacitive soil moisture sensor to the Adafruit Feather nRF52 safely and correctly.

Follow these steps in order. Do not skip steps.

What you should have
1. Adafruit Feather nRF52 (powered off)
2. Capacitive soil moisture sensor (STEMMA / I²C)
3. STEMMA / JST cable (or jumper wires)
4. USB cable (for the Feather)
5. A houseplant with soil (dry is best for first test)

## Part 1: Power safety (important)

Before connecting anything:
- The Feather is not plugged into USB
- No battery is connected
- The sensor is not powered

Never hot-plug the sensor while the Feather is powered.

## Part 2: Identify the Feather pins

On the Feather nRF52, locate:
- 3V → 3.3V power
- GND → ground
- SDA → I²C data
- SCL → I²C clock

These labels are printed on the board.

## Part 3: Identify the sensor pins

On the capacitive soil moisture sensor, locate:
- VIN or 3V
- GND
- SDA
- SCL

Most Adafruit STEMMA sensors use I²C and are labeled clearly.

## Part 4: Wire the sensor to the Feather

Connect pin-to-pin as follows:
- Feather 3V → Sensor VIN / 3V
- Feather GND → Sensor GND
- Feather SDA → Sensor SDA
- Feather SCL → Sensor SCL

Double-check all four connections before continuing.

## Part 5: Common mistakes to avoid (read this)

- Do not connect the sensor to 5V
- Do not swap SDA and SCL
- Do not power the Feather until wiring is complete
- Do not insert the probe into soil while the board is loose on a desk

If anything smells hot or gets warm, unplug immediately.

## Part 6: Power on and verify I²C detection

1. Plug the Feather into USB.
2. Open Arduino IDE.
3. Open the I²C scanner sketch: `firmware/i2c_scanner/i2c_scanner.ino`
4. Upload the sketch.
5. Open Serial Monitor.
6. Set baud rate to 115200.

Expected output:
- A detected I²C device address (for example: 0x36)
- The scanner repeats every few seconds

If no devices are found:
- Recheck wiring
- Confirm SDA and SCL are correct
- Confirm the sensor is an I²C device

Do not continue until the sensor is detected.

## Part 7: Insert the probe into soil

- Insert only the sensor probe portion into soil
- Keep the Feather board and cable above the soil
- Do not bend the probe sharply

## Part 8: Prepare for firmware integration

Once the sensor is detected via I²C:
- Wiring is confirmed correct
- Sensor responds consistently
- Ready to replace stubbed moisture value in firmware

At this point, the hardware is ready for:
- Real moisture readings
- Calibration
- Threshold logic

Stop here until firmware integration begins.

## Success criteria (stop here)

You are done when:
1. Sensor is detected by I²C scanner
2. No overheating or power issues
3. Probe is safely inserted in soil
4. Feather remains stable when powered

Notes:
- Moisture values are not yet calibrated
- Calibration will be handled in a later step
- This checklist only validates wiring and detection