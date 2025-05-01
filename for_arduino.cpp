#include <SoftwareSerial.h>
#include <Adafruit_Fingerprint.h>

SoftwareSerial fingerSerial(2, 3); // RX, TX for fingerprint
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerSerial);

SoftwareSerial espSerial(10, 11); // RX, TX for ESP8266

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  espSerial.begin(9600);

  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor connected.");
  } else {
    Serial.println("Fingerprint sensor not found.");
    while (1);
  }
}

void loop() {
  getFingerprintID();
  delay(1000);
}

int getFingerprintID() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.print("Found ID: "); Serial.println(finger.fingerID);
    sendToESP(finger.fingerID);
    return finger.fingerID;
  }

  return -1;
}

void sendToESP(int id) {
  String data = "ID:" + String(id);
  espSerial.println(data);
}
