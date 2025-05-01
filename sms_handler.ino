
#include <SoftwareSerial.h>

SoftwareSerial sim800(10, 11); // RX, TX for SIM800L

void setup() {
  Serial.begin(9600);
  sim800.begin(9600);
  delay(1000);

  sim800.println("AT+CMGF=1"); // Set SMS to text mode
  delay(1000);
  sim800.println("AT+CNMI=1,2,0,0,0"); // Forward SMS to Serial
  delay(1000);
}

void loop() {
  if (sim800.available()) {
    Serial.write(sim800.read());
  }
  if (Serial.available()) {
    sim800.write(Serial.read());
  }
}
