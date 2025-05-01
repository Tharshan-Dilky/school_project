
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar
import csv
import datetime

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
today = datetime.date.today().isoformat()

root = tk.Tk()
root.title("Attendance Admin Dashboard")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

student_tab = ttk.Frame(notebook)
attendance_tab = ttk.Frame(notebook)
reply_tab = ttk.Frame(notebook)

notebook.add(student_tab, text='Student List')
notebook.add(attendance_tab, text='Today\'s Attendance')
notebook.add(reply_tab, text='Parent Replies')

def update_student_list():
    for i in tree_students.get_children():
        tree_students.delete(i)
    cursor.execute("SELECT id, name, class, fingerprint_id FROM students")
    for row in cursor.fetchall():
        tree_students.insert("", "end", values=row)

def add_student():
    def save_student():
        name = name_entry.get()
        student_class = class_entry.get()
        fingerprint_id = fingerprint_entry.get()
        parent_phone = phone_entry.get()

        if name and student_class and fingerprint_id and parent_phone:
            cursor.execute("INSERT INTO students (name, class, fingerprint_id, parent_phone) VALUES (?, ?, ?, ?)",
                           (name, student_class, fingerprint_id, parent_phone))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            add_window.destroy()
            update_student_list()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    add_window = tk.Toplevel(root)
    add_window.title("Add Student")

    tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(add_window, text="Class:").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(add_window, text="Fingerprint ID:").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(add_window, text="Parent Phone:").grid(row=3, column=0, padx=10, pady=10)

    name_entry = tk.Entry(add_window)
    class_entry = tk.Entry(add_window)
    fingerprint_entry = tk.Entry(add_window)
    phone_entry = tk.Entry(add_window)

    name_entry.grid(row=0, column=1, padx=10, pady=10)
    class_entry.grid(row=1, column=1, padx=10, pady=10)
    fingerprint_entry.grid(row=2, column=1, padx=10, pady=10)
    phone_entry.grid(row=3, column=1, padx=10, pady=10)

    save_button = ttk.Button(add_window, text="Save", command=save_student)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

add_student_button = ttk.Button(student_tab, text="Add Student", command=add_student)
add_student_button.pack(pady=10)

tree_students = ttk.Treeview(student_tab, columns=("ID", "Name", "Class", "Fingerprint"), show='headings')
for col in tree_students["columns"]:
    tree_students.heading(col, text=col)
tree_students.pack(fill='both', expand=True)

update_student_list()

calendar = Calendar(attendance_tab, selectmode='day', date_pattern='yyyy-mm-dd')
calendar.pack(pady=20)

tree_attendance = ttk.Treeview(attendance_tab, columns=("ID", "Name", "Status"), show='headings')
for col in tree_attendance["columns"]:
    tree_attendance.heading(col, text=col)
tree_attendance.pack(fill='both', expand=True)

def fetch_attendance():
    selected_date = calendar.get_date()
    for row in tree_attendance.get_children():
        tree_attendance.delete(row)
    cursor.execute('''
        SELECT s.id, s.name, a.status 
        FROM students s 
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
    ''', (selected_date,))
    for row in cursor.fetchall():
        status = row[2] if row[2] else "absent"
        tree_attendance.insert("", "end", values=(row[0], row[1], status))

view_button = ttk.Button(attendance_tab, text="View Attendance", command=fetch_attendance)
view_button.pack(pady=10)

def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Attendance Report")
    if file_path:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Status"])
            for row_id in tree_attendance.get_children():
                writer.writerow(tree_attendance.item(row_id)["values"])
        messagebox.showinfo("Success", "Attendance exported successfully!")

export_btn = ttk.Button(attendance_tab, text="Export to CSV", command=export_csv)
export_btn.pack(pady=10)

tree_replies = ttk.Treeview(reply_tab, columns=("Student", "Reason"), show='headings')
for col in tree_replies["columns"]:
    tree_replies.heading(col, text=col)
tree_replies.pack(fill='both', expand=True)

cursor.execute('''
    SELECT s.name, r.reason FROM students s
    JOIN replies r ON s.id = r.student_id
    WHERE r.date = ?
''', (today,))
for row in cursor.fetchall():
    tree_replies.insert("", "end", values=row)

root.mainloop()
conn.close()
