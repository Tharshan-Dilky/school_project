import sqlite3

with open("database_setup.sql", "r") as f:
    sql_script = f.read()

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()
