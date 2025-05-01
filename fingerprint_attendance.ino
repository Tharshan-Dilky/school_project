
#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

SoftwareSerial fingerSerial(2, 3); // RX, TX for R307
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerSerial);

SoftwareSerial sim800(10, 11); // RX, TX for SIM800L

void setup() {
  Serial.begin(9600);
  finger.begin(57600);

  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor found!");
  } else {
    Serial.println("Fingerprint sensor not found :(");
    while (1);
  }

  sim800.begin(9600);
  delay(1000);
  sim800.println("AT");
  delay(1000);
  sim800.println("AT+CMGF=1"); // Text mode
  delay(1000);
}

void loop() {
  getFingerprintID();
  delay(50);
}

int getFingerprintID() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.fingerSearch();
  if (p != FINGERPRINT_OK) {
    Serial.println("Finger not found");
    return -1;
  }

  int id = finger.fingerID;
  Serial.print("Found ID #"); Serial.println(id);

  sendToPython(id);

  return id;
}

void sendToPython(int id) {
  Serial.print("ID:");
  Serial.println(id);
}
