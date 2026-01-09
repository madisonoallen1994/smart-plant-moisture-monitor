#include <bluefruit.h>

// v0 BLE identity
static const char* DEVICE_NAME = "Plant";

// v0 UUIDs (must match docs/contracts.md)
static const char* SERVICE_UUID_STR = "12345678-1234-1234-1234-1234567890ab";
static const char* CHAR_UUID_STR    = "12345678-1234-1234-1234-1234567890ac";

// BLE objects
BLEService        moistureService(SERVICE_UUID_STR);
BLECharacteristic latestReadingChar(CHAR_UUID_STR);

// v0 payload fields
static const char* PROBE_ID   = "probe-001";
static const char* FW_VERSION = "0.1.0";

// For v0 we stub moistureRaw until the sensor is wired
static int readMoistureRawStub() {
  return 500;
}

// Build UTF-8 JSON string for characteristic value.
// Keep it small and deterministic.
static void buildPayload(char* outBuf, size_t outSize) {
  int moistureRaw = readMoistureRawStub();

  // Example v0 probe-side payload (hub will add timestamp when POSTing)
  // {
  //   "probeId":"probe-001",
  //   "moistureRaw":500,
  //   "fwVersion":"0.1.0"
  // }
  snprintf(
    outBuf,
    outSize,
    "{\"probeId\":\"%s\",\"moistureRaw\":%d,\"fwVersion\":\"%s\"}",
    PROBE_ID,
    moistureRaw,
    FW_VERSION
  );
}


void setup() {
  Serial.begin(115200);
  delay(200);

  // Initialize Bluefruit stack
  Bluefruit.begin();
  Bluefruit.setTxPower(4); // modest default
  Bluefruit.setName(DEVICE_NAME);

  // Optional: show basic info
  Serial.println("BLE GATT MVP starting...");
  Serial.print("Device name: ");
  Serial.println(DEVICE_NAME);

  // Set up GATT Service + Characteristic
  moistureService.begin();

  // Characteristic properties: READ (required), NOTIFY (optional but helpful)
  latestReadingChar.setProperties(CHR_PROPS_READ | CHR_PROPS_NOTIFY);
  latestReadingChar.setPermission(SECMODE_OPEN, SECMODE_NO_ACCESS);

  // Max size for JSON payload
  latestReadingChar.setMaxLen(160);

  // Start the characteristic FIRST
  latestReadingChar.begin();

  // Initialize value once (after begin)
  char payload[160];
  buildPayload(payload, sizeof(payload));
  latestReadingChar.write((uint8_t*)payload, strlen(payload));

  // Advertising
  Bluefruit.Advertising.stop();
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include our service UUID so scanners can find it
  Bluefruit.Advertising.addService(moistureService);

  // Also advertise the device name
  Bluefruit.Advertising.addName();

  // Restart advertising automatically on disconnect
  Bluefruit.Advertising.restartOnDisconnect(true);

  // Advertising interval (in units of 0.625ms). These are reasonable defaults.
  Bluefruit.Advertising.setInterval(32, 244); // fast to slow
  Bluefruit.Advertising.setFastTimeout(30);   // seconds of fast adv

  Bluefruit.Advertising.start(0); // 0 = advertise forever

  Serial.println("Advertising started.");
  Serial.print("Service UUID: ");
  Serial.println(SERVICE_UUID_STR);
  Serial.print("Char UUID: ");
  Serial.println(CHAR_UUID_STR);
}

void loop() {
  static uint32_t lastUpdateMs = 0;
  const uint32_t updateIntervalMs = 2000; // keep fresh for read-based hub

  uint32_t now = millis();
  if (now - lastUpdateMs >= updateIntervalMs) {
    lastUpdateMs = now;

    char payload[160];
    buildPayload(payload, sizeof(payload));

    // Always keep characteristic value up to date for GATT reads
    latestReadingChar.write((uint8_t*)payload, strlen(payload));

    // Only notify if a central subscribed
    if (Bluefruit.connected() && latestReadingChar.notifyEnabled()) {
      latestReadingChar.notify((uint8_t*)payload, strlen(payload));
      Serial.print("Notify payload: ");
      Serial.println(payload);
    } else {
      Serial.print("Updated value (no notify): ");
      Serial.println(payload);
    }
  }

  delay(20);
}
