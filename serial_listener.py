
import serial
import sqlite3
import datetime
import time

# Connect to SQLite database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Set up serial connection to Arduino
arduino = serial.Serial("COM3", 9600, timeout=1)  # Replace COM3 with your Arduino port
time.sleep(2)  # Wait for Arduino to reset

def mark_attendance(student_id):
    today = datetime.date.today().isoformat()
    cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, today))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                       (student_id, today, "present"))
        conn.commit()
        print(f"Marked present for student ID {student_id}")
    else:
        print(f"Already marked for student ID {student_id}")

def check_absentees():
    today = datetime.date.today().isoformat()
    cursor.execute("SELECT id, parent_phone FROM students")
    all_students = cursor.fetchall()
    for sid, phone in all_students:
        cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (sid, today))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                           (sid, today, "absent"))
            conn.commit()
            send_sms(phone, f"Your child (ID: {sid}) is absent today. Please reply with a reason.")

def send_sms(phone_number, message):
    sim = serial.Serial("COM4", 9600, timeout=1)  # Replace COM4 with SIM800L port
    time.sleep(1)
    sim.write(b'AT+CMGF=1\r')
    time.sleep(1)
    sim.write(f'AT+CMGS="{phone_number}"\r'.encode())
    time.sleep(1)
    sim.write(f"{message}".encode())
    time.sleep(3)
    sim.close()
    print(f"SMS sent to {phone_number}")

def listen_for_ids():
    print("Listening for fingerprint IDs...")
    try:
        while True:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode().strip()
                if line.startswith("ID:"):
                    student_id = int(line.split(":")[1])
                    mark_attendance(student_id)
    except KeyboardInterrupt:
        arduino.close()
        conn.close()

# Run at 8:00 AM daily to mark absentees
current_time = datetime.datetime.now().time()
if current_time < datetime.time(8, 0):
    listen_for_ids()
else:
    check_absentees()
