# 🧠 LOGIC FLOW 
1. Student places finger → Arduino + R307 identifies student.

2. Arduino checks current time.

3. If time < 8:00 AM → mark present.

4. If late/missed → mark absent + send SMS via SIM800L.

5. Arduino sends student ID + status to server via ESP8266.

6. Tkinter dashboard syncs with server and shows status.

7. Parent can reply to SMS manually, and teacher can add that info in the dashboard.

# 🧰 HARDWARE NEEDED
<table>
    <tr><th>Component</th><th> Notes</th></tr>	                           
      <tr><td>R307</td><td>Fingerprint sensor (with TTL wires)</td></tr>
      <tr><td>ESP8266 (NodeMCU)	</td><td> Wi-Fi board to send data</td></tr>
      <tr><td>SIM800L</td><td>GSM module to send SMS</td></tr>
      <tr><td>Arduino UNO/Nano</td><td>For R307 + SIM800L integration</td></tr>
    <tr><td>Power supply</td><td>5V/2A for stable operation</td></tr>
    <tr><td>Level shifter</td><td>For SIM800L (optional but safer)</td></tr>
    <tr><td>PC/Laptop</td><td>To run Tkinter GUI + SQLite DB</td></tr>
  </table>

# 🔌 HARDWARE CONNECTIONS
## R307 → Arduino

 TX → D2 (via SoftwareSerial RX)

 RX → D3 (via SoftwareSerial RX)

 VCC → 5V

 GND → GND

## SIM800L → Arduino (via SoftwareSerial)

 TX → D10 (SoftwareSerial RX)

 RX → D11 (SoftwareSerial RX)

 VCC → External 4V power supply (not from Arduino!)

 GND → GND(shared with arduino)

 > ⚠️ SIM800L is sensitive to voltage. Use a 4V 2A power supply.

## ESP8266 (NodeMCU or ESP-01) → Arduino UNO
+ Connect via UART or SoftwareSerial

+ Example using TX/RX:

    + ESP8266 TX → Arduino RX

    + ESP8266 RX → Arduino TX (use voltage divider to drop 5V to 3.3V)

OR connect ESP8266 directly to internet via HTTP from Arduino sketch using AT commands (if using ESP-01).

## 💻 SOFTWARES NEEDED
Software_______________________________Purpose

Arduino IDE             -------------->	Upload code to Arduino

XAMPP	                -------------->Local PHP + MySQL Server

Python 3.x    	        -------------->To run GUI

Required Python libs	-------------->tkinter, sqlite3

Browser                 -------------->	Access PHP script (via IP)


## 📁 CODES PROVIDED
1. r307_fingerprint.ino
    + Handles fingerprint enrollment + matching

2. esp8266_attendance.ino
    + Sends data via HTTP

    + Sends SMS via SIM800L

    + Logic for time check, ID detection

3. attendance.php
    + Accepts HTTP POST request and writes to MySQL

4. create_attendance_table.sql
    + SQL to create attendance table in MySQL

5. tkinter_dashboard.py
    + PC GUI to view/edit attendance

    + Uses attendance.db SQLite file
# 🌐 SERVER SETUP
Install XAMPP

Start Apache + MySQL

Create database attendance in phpMyAdmin

Import create_attendance_table.sql

Place attendance.php in:
```swift
C:/xampp/htdocs/attendance/attendance.php
```
Open it and update DB credentials if needed

Get your local IP (e.g., 192.168.1.5) and use:
```arduino
http://192.168.x.x/attendance/attendance.php
```
## 📡 ESP8266 CODE
Connect to Wi-Fi

Send HTTP POST request to PHP script

Data: student_id, status

✅ Already included in esp8266_attendance.ino

## 📲 SMS WITH SIM800L
Pre-configured to send SMS when student is marked absent

Parents reply (optional) — you can manually feed reply into SQLite

✅ Already included in esp8266_attendance.ino

## 🧑‍🏫 PC SIDE: GUI DASHBOARD
Use the tkinter_dashboard.py provided

It reads/writes from attendance.db (SQLite)

You can use this dashboard to:

View who was present/absent

Mark/update reasons

Export reports later if needed


## ✅ FINAL SETUP AT SCHOOL GATE
+ Mount:

    + R307 + Arduino + ESP8266 + SIM800L in a box

+ Power:

    + Stable 5V/2A adapter

+ Network:

    + Connect ESP8266 to school Wi-Fi

+ Server:

    + PC inside office runs Apache/MySQL + PHP

    + Use local IP as endpoint

+ Dashboard:

    + Tkinter dashboard runs on office PC

## 📦 PROJECT FILES INCLUDED:
File_______________________________________________Description

esp8266_attendance.ino	    -------------->    ESP8266 + SIM800L HTTP + SMS logic

r307_fingerprint.ino	    -------------->    Arduino + R307 code

attendance.php            	-------------->    Server-side script for logging data

create_attendance_table.sql	-------------->    SQL to create the MySQL table

tkinter_dashboard.py        -------------->    Desktop GUI with SQLite


## 📁 CODES PROVIDED
1. r307_fingerprint.ino
    + Handles fingerprint enrollment + matching

2. esp8266_attendance.ino
    + Sends data via HTTP

    + Sends SMS via SIM800L

    + Logic for time check, ID detection

3. attendance.php
    + Accepts HTTP POST request and writes to MySQL

4. create_attendance_table.sql
    + SQL to create attendance table in MySQL

5. tkinter_dashboard.py
    + PC GUI to view/edit attendance

    + Uses attendance.db SQLite file


