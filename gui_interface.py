import tkinter as tk
from tkinter import messagebox
from face_registration import register_face
from mark_attendance import mark_attendance  


def register_student_gui():
    def register():
        name = name_entry.get()
        roll_no = roll_no_entry.get()
        if name and roll_no:
            register_face(name, roll_no)
            messagebox.showinfo("Success", "Face registered successfully!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    reg_window = tk.Toplevel()
    reg_window.title("Register Student")
    tk.Label(reg_window, text="Name").grid(row=0, column=0)
    tk.Label(reg_window, text="Roll No").grid(row=1, column=0)
    name_entry = tk.Entry(reg_window)
    roll_no_entry = tk.Entry(reg_window)
    name_entry.grid(row=0, column=1)
    roll_no_entry.grid(row=1, column=1)
    tk.Button(reg_window, text="Register", command=register).grid(row=2, column=0, columnspan=2)

def main_gui():
    root = tk.Tk()
    root.title("Attendance Management System")
    tk.Button(root, text="Register Student", command=register_student_gui).pack(pady=10)
    tk.Button(root, text="Mark Attendance", command=mark_attendance).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main_gui()
