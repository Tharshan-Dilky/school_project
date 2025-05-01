import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    student_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    reason TEXT)""")
    conn.commit()
    conn.close()

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close()

def mark_reason():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a student")
        return
    reason = reason_entry.get()
    if not reason:
        messagebox.showwarning("No Reason", "Please enter a reason")
        return
    item = tree.item(selected[0])
    attendance_id = item['values'][0]

    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("UPDATE attendance SET reason = ? WHERE id = ?", (reason, attendance_id))
    conn.commit()
    conn.close()
    load_data()
    reason_entry.delete(0, tk.END)
    messagebox.showinfo("Updated", "Reason updated successfully")

# GUI setup
connect_db()
root = tk.Tk()
root.title("School Attendance Dashboard")
root.geometry("800x500")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Student ID", "Name", "Date", "Status", "Reason")
tree = ttk.Treeview(frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

refresh_button = ttk.Button(root, text="Refresh", command=load_data)
refresh_button.pack(pady=5)

reason_label = ttk.Label(root, text="Update Reason:")
reason_label.pack()
reason_entry = ttk.Entry(root, width=40)
reason_entry.pack()

update_button = ttk.Button(root, text="Submit Reason", command=mark_reason)
update_button.pack(pady=5)

load_data()
root.mainloop()
