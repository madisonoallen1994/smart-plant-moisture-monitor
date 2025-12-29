#include <Arduino.h>
#include <Wire.h>

// Adafruit Bluefruit nRF52 library (comes with Adafruit nRF52 Boards package)
#include <bluefruit.h>

static const char* PROBE_ID = "probe-001";
static const char* FW_VERSION = "0.1.0";

// v0: Stable 128-bit UUIDs (do not change once the hub depends on them)
BLEService plantService("12345678-1234-1234-1234-1234567890ab");
BLECharacteristic latestReadingChar("12345678-1234-1234-1234-1234567890ac");

int readMoistureRawPlaceholder() {
  // Placeholder until the I2C sensor read is implemented in Step 2.1.
  // Keep this boring for now; we just want BLE working.
  return 500;
}

void setupBLE() {
  Bluefruit.begin();
  Bluefruit.setName("PlantProbe");

  plantService.begin();

  // "Latest Reading" characteristic: read + notify
  latestReadingChar.setProperties(CHR_PROPS_READ | CHR_PROPS_NOTIFY);
  latestReadingChar.setPermission(SECMODE_OPEN, SECMODE_NO_ACCESS);

  // Variable length, but cap it to avoid accidental huge payloads
  latestReadingChar.setFixedLen(0);
  latestReadingChar.setMaxLen(200);
  latestReadingChar.begin();

  // Advertising
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addService(plantService);
  Bluefruit.Advertising.addName();

  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(160, 160); // 100 ms
  Bluefruit.Advertising.setFastTimeout(30);
  Bluefruit.Advertising.start(0);
}

void publishLatestReading() {
  int moistureRaw = readMoistureRawPlaceholder();

  // v0: JSON string for easy debugging in nRF Connect + hub logs
  char payload[200];
  snprintf(payload, sizeof(payload),
           "{\"probeId\":\"%s\",\"moistureRaw\":%d,\"fwVersion\":\"%s\"}",
           PROBE_ID, moistureRaw, FW_VERSION);

  latestReadingChar.write((const uint8_t*)payload, strlen(payload));
  latestReadingChar.notify((const uint8_t*)payload, strlen(payload));

  Serial.println(payload);
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  Wire.begin(); // for later I2C sensor reads

  setupBLE();
  Serial.println("Probe BLE GATT MVP started");
}

void loop() {
  // Bench test loop: publish every 5 seconds.
  // Step 2.3 will replace this with wake → read → advertise/notify → sleep.
  publishLatestReading();
  delay(5000);
}
