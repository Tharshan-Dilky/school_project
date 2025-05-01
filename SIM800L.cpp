void sendSMS(String phone, String msg) {
  Serial.println("AT+CMGF=1");    // Text mode
  delay(100);
  Serial.println("AT+CMGS=\"" + phone + "\"");
  delay(100);
  Serial.print(msg);
  delay(100);
  Serial.write(26); // Ctrl+Z to send
}
