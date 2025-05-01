##  ✅ 8. Hardware Wiring Summary

| Component       | Connected To (Arduino Uno)                |
|----------------|--------------------------------------------|
| R307 TX         | Pin 2                                      |
| R307 RX         | Pin 3                                      |
| ESP8266 RX      | Pin 10 (via voltage divider)               |
| ESP8266 TX      | Pin 11                                     |
| SIM800L TX      | Use SoftwareSerial                         |
| SIM800L RX      | Via level shifter or voltage divider       |
| 5V / 3.3V Power  | Use external power source                 |
