#include <SoftwareSerial.h>
SoftwareSerial espSerial(2, 3); // RX, TX (connect to Arduino)

String server = "http://your-server.com/mark_attendance.php";

void setup() {
  Serial.begin(9600);
  espSerial.begin(9600);
  connectWiFi();
}

void loop() {
  if (espSerial.available()) {
    String data = espSerial.readStringUntil('\n');
    Serial.println("Received: " + data);
    int idIndex = data.indexOf("ID:");
    if (idIndex != -1) {
      String idStr = data.substring(idIndex + 3);
      sendToServer(idStr);
    }
  }
}

void connectWiFi() {
  Serial.println("Connecting to WiFi...");
  // Add AT commands to connect to WiFi
}

void sendToServer(String id) {
  // Replace with HTTP GET or POST request code using AT commands
  Serial.println("Sending to server: " + server + "?id=" + id);
}
