import tkinter as tk
from tkinter import ttk, Toplevel, Frame, Label, Button, messagebox , Scrollbar
from PIL import Image, ImageTk
import sqlite3
from patient_form import Patient
from room_form import Room
from employee_form import Employee
from appointment_form import Appointment
from billing_form import Billing
import hashlib
import requests
import database

class CustomEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        ttk.Entry.__init__(self, master, **kwargs)
        self['style'] = 'Custom.TEntry'

def set_custom_style():
    style = ttk.Style()
    style.configure('Custom.TEntry', padding=(10, 5), font=('Helvetica', 14), foreground='black')
    style.configure('Custom.TButton', padding=(10, 5), font=('Helvetica', 12), foreground='white', background='#4CAF50')

# Initialize the database on startup
database.initialize_db()
conn = database.get_connection()
print("DATABASE CONNECTION SUCCESSFUL")

class EditAppointmentForm:
    def __init__(self, master, appointment_id, view_appointments_callback):
        self.view_appointments_callback = view_appointments_callback
        self.master = master
        self.master.title("Edit Appointment")
        self.master.geometry("400x600")

        self.appointment_id = appointment_id

        self.lblTitle = Label(self.master, text="Edit Appointment Information", font=("Helvetica", 16))
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=10)

        self.column_names = self.get_column_names()
        self.entry_widgets = {}

        for i, column_name in enumerate(self.column_names):
            label = Label(self.master, text=f"{column_name.capitalize()}:")
            label.grid(row=i + 1, column=0, pady=5, padx=10, sticky='e')

            entry = CustomEntry(self.master)
            entry.grid(row=i + 1, column=1, pady=5, padx=10, sticky='w')

            self.entry_widgets[column_name] = entry

        self.btnSave = Button(self.master, text="Save Changes", command=self.save_changes)
        self.btnSave.grid(row=len(self.column_names) + 1, column=0, columnspan=2, pady=20)

        self.fetch_appointment_details()

    def get_column_names(self):
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(appointment)")
            column_names = [column[1] for column in cursor.fetchall()]
            return column_names
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching column names: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_appointment_details(self):
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM appointment WHERE PATIENT_ID=?", (self.appointment_id,))
            appointment_details = cursor.fetchone()

            if appointment_details:
                for column_name, value in zip(self.column_names, appointment_details):
                    self.entry_widgets[column_name].insert(0, value)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching appointment details: {e}")
        finally:
            if cursor:
                cursor.close()

    def save_changes(self):
        try:
            cursor = conn.cursor()

            # Create SET statement for dynamic update
            set_statement = ", ".join(f"{column_name} = ?" for column_name in self.column_names)

            # Update the appointment details in the database
            cursor.execute(f"UPDATE appointment SET {set_statement} WHERE APPOINTMENT_ID=?",
                           tuple(entry.get() for entry in self.entry_widgets.values()) + (self.appointment_id,))
            conn.commit()

            messagebox.showinfo("Success", "Appointment information updated successfully!")

            # Close the edit window
            self.master.destroy()

            # Trigger the callback to refresh the "View Appointments" window
            if self.view_appointments_callback:
                self.view_appointments_callback()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating appointment information: {e}")
        finally:
            if cursor:
                cursor.close()
class EditEmployeeForm:
    def __init__(self, master, employee_id, view_employees_callback):
        self.view_employees_callback = view_employees_callback
        self.master = master
        self.master.title("Edit Employee")
        self.master.geometry("400x600")

        self.employee_id = employee_id

        self.lblTitle = Label(self.master, text="Edit Employee Information", font=("Helvetica", 16))
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=10)

        self.column_names = self.get_column_names()
        self.entry_widgets = {}

        for i, column_name in enumerate(self.column_names):
            label = Label(self.master, text=f"{column_name.capitalize()}:")
            label.grid(row=i + 1, column=0, pady=5, padx=10, sticky='e')

            entry = CustomEntry(self.master)
            entry.grid(row=i + 1, column=1, pady=5, padx=10, sticky='w')

            self.entry_widgets[column_name] = entry

        self.btnSave = Button(self.master, text="Save Changes", command=self.save_changes)
        self.btnSave.grid(row=len(self.column_names) + 1, column=0, columnspan=2, pady=20)

        self.fetch_employee_details()

    def get_column_names(self):
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(employee)")
            column_names = [column[1] for column in cursor.fetchall()]
            return column_names
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching column names: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_employee_details(self):
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM employee WHERE EMP_ID=?", (self.employee_id,))
            employee_details = cursor.fetchone()

            if employee_details:
                for column_name, value in zip(self.column_names, employee_details):
                    self.entry_widgets[column_name].insert(0, value)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching employee details: {e}")
        finally:
            if cursor:
                cursor.close()

    def save_changes(self):
        try:
            cursor = conn.cursor()

            set_statement = ", ".join(f"{column_name} = ?" for column_name in self.column_names)

            cursor.execute(f"UPDATE employee SET {set_statement} WHERE EMP_ID=?",
                           tuple(entry.get() for entry in self.entry_widgets.values()) + (self.employee_id,))
            conn.commit()

            messagebox.showinfo("Success", "Employee information updated successfully!")

            self.master.destroy()

            if self.view_employees_callback:
                self.view_employees_callback()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating employee information: {e}")
        finally:
            if cursor:
                cursor.close()
# ... (previous code)

class EditPatientForm:
    def __init__(self, master, patient_id, view_patients_callback):
        self.view_patients_callback = view_patients_callback
        self.master = master
        self.master.title("Edit Patient")
        self.master.geometry("400x600")

        self.patient_id = patient_id

        self.lblTitle = Label(self.master, text="Edit Patient Information", font=("Helvetica", 16))
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=10)

        self.column_names = self.get_column_names()
        self.entry_widgets = {}

        for i, column_name in enumerate(self.column_names):
            label = Label(self.master, text=f"{column_name.capitalize()}:")
            label.grid(row=i + 1, column=0, pady=5, padx=10, sticky='e')

            if column_name == 'BLOOD_GROUP':
                # For the 'blood_group' column, use a Combobox
                values = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                combobox = ttk.Combobox(self.master, values=values)
                combobox.grid(row=i + 1, column=1, pady=5, padx=10, sticky='w')
                self.entry_widgets[column_name] = combobox
            else:
                entry = CustomEntry(self.master)
                entry.grid(row=i + 1, column=1, pady=5, padx=10, sticky='w')
                self.entry_widgets[column_name] = entry

        self.btnSave = Button(self.master, text="Save Changes", command=self.save_changes)
        self.btnSave.grid(row=len(self.column_names) + 1, column=0, columnspan=2, pady=20)

        self.fetch_patient_details()

    def get_column_names(self):
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(patient)")
            column_names = [column[1] for column in cursor.fetchall()]
            return column_names
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching column names: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_patient_details(self):
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM patient WHERE PATIENT_ID=?", (self.patient_id,))
            patient_details = cursor.fetchone()

            if patient_details:
                for column_name, value in zip(self.column_names, patient_details):
                    if column_name == 'blood_group':
                        # For 'blood_group', set the selected value in the Combobox
                        self.entry_widgets[column_name].set(value)
                    else:
                        self.entry_widgets[column_name].insert(0, value)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching patient details: {e}")
        finally:
            if cursor:
                cursor.close()

    def save_changes(self):
        try:
            cursor = conn.cursor()

            # Create SET statement for dynamic update
            set_statement = ", ".join(f"{column_name} = ?" for column_name in self.column_names)

            # Update the patient details in the database
            cursor.execute(f"UPDATE patient SET {set_statement} WHERE PATIENT_ID=?",
                           tuple(entry.get() if column_name != 'blood_group' else entry.get() for column_name, entry in self.entry_widgets.items()) + (self.patient_id,))
            conn.commit()

            messagebox.showinfo("Success", "Patient information updated successfully!")

            # Close the edit window
            self.master.destroy()

            # Trigger the callback to refresh the "View Patients" window
            if self.view_patients_callback:
                self.view_patients_callback()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating patient information: {e}")
        finally:
            if cursor:
                cursor.close()

# ... (previous code)

class HospitalMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("800x900+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()

        self.lblTitle = Label(self.frame, text="Main Menu", font=("Impact", 30), bg="#E9ECF3", fg="#1a237e")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="flat", bg="#E9ECF3")
        self.LoginFrame.grid(row=1, column=0)
        self.button8 = Button(self.LoginFrame, text="View Employees", width=30, font="Arial", fg="white",
                              bg="#740048", pady=7, command=self.View_Employees)
        self.button8.grid(row=7, column=0, pady=10)

        self.button1 = Button(self.LoginFrame, text="Patient Registrations", width=30, font="Arial", fg="white",
                              bg="#AF006C", pady=7, command=self.Patient_Reg)
        self.button1.grid(row=1, column=0, pady=10)

        self.button2 = Button(self.LoginFrame, text="Room Allocation", width=30, font="Arial", fg="white",
                              bg="#AF006C", pady=7, command=self.Room_Allocation)
        self.button2.grid(row=13, column=0, pady=10)

        self.button3 = Button(self.LoginFrame, text="Employee Registration", width=30, font="Arial", fg="white",
                              bg="#AF006C", pady=7, command=self.Employee_Reg)
        self.button3.grid(row=5, column=0, pady=10)

        self.button4 = Button(self.LoginFrame, text="Book Appointment", width=30, font="Arial", fg="white",
                              bg="#AF006C", pady=7, command=self.Appointment_Form)
        self.button4.grid(row=9, column=0, pady=10)

        self.button5 = Button(self.LoginFrame, text="Patient Bill", width=30, font="Arial", fg="white",
                              bg="#740048", pady=7, command=self.Billing_Form)
        self.button5.grid(row=15, column=0, pady=10)

        self.button6 = Button(self.LoginFrame, text="Exit", width=30, font="Arial", fg="white",
                              bg="#AF006C", pady=7, command=self.Exit)
        self.button6.grid(row=17, column=0, pady=10)

        self.button7 = Button(self.LoginFrame, text="View Patients", width=30, font="Arial", fg="white",
                              bg="#740048", pady=7, command=self.View_Patients)
        self.button7.grid(row=3, column=0, pady=10)

        self.button8 = Button(self.LoginFrame, text="View Employees", width=30, font="Arial", fg="white",
                              bg="#740048", pady=7, command=self.View_Employees)
        self.button8.grid(row=7, column=0, pady=10)

        self.button9 = Button(self.LoginFrame, text="View Appointments", width=30, font="Arial", fg="white",
                              bg="#740048", pady=7, command=self.View_Appointments)
        self.button9.grid(row=11, column=0, pady=10)

    def Exit(self):
        self.master.destroy()

    def Patient_Reg(self):
        self.newWindow = Toplevel(self.master)
        self.app = Patient(self.newWindow)

    def Room_Allocation(self):
        self.newWindow = Toplevel(self.master)
        self.app = Room(self.newWindow)

    def Employee_Reg(self):
        self.newWindow = Toplevel(self.master)
        self.app = Employee(self.newWindow)

    def Appointment_Form(self):
        self.newWindow = Toplevel(self.master)
        self.app = Appointment(self.newWindow)

    def Billing_Form(self):
        self.newWindow = Toplevel(self.master)
        self.app = Billing(self.newWindow)

    def View_Patients(self):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient")
            patients = cursor.fetchall()

            if not patients:
                messagebox.showinfo("View Patients", "No patients found.")
                return

            self.newWindow = Toplevel(self.master)
            self.newWindow.title("All Patients")
            self.newWindow.geometry("800x600")
            self.newWindow.config(bg="#d3d3d3")

            # Create a frame to hold the Treeview and scrollbar
            frame = Frame(self.newWindow)
            frame.pack(expand=True, fill="both")

            tree = ttk.Treeview(frame)
            tree["columns"] = tuple("col" + str(i) for i in range(len(patients[0])))
            tree["show"] = "headings"

            # Change the header names
            header_names = ["Patient ID"] + ["Name", "Sex", "Blood Group", "Date Of Birth", "Address", "Consult Team", "Email"]

            for i, heading in enumerate(header_names):
                tree.heading("col" + str(i), text=heading)
                tree.column("col" + str(i), anchor="center")

            for patient in patients:
                tree.insert("", "end", values=patient)

            tree.pack(side="top", expand=True, fill="both")

            # Add horizontal scrollbar
            scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            tree.configure(xscrollcommand=scrollbar_x.set)

            # Add an 'Edit' button
            edit_button = ttk.Button(self.newWindow, text="Edit", command=lambda: self.edit_patient(tree))
            edit_button.pack(pady=10)

            # Set the background and foreground color of the "Edit" button
            edit_button.configure(style='Custom.TButton', background='lavender', foreground='black')

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching patients: {e}")
        finally:
            if cursor:
                cursor.close()
    def edit_patient(self, tree):
        # Get the selected item
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Edit Patient", "Please select a patient to edit.")
            return

        # Assuming the patient ID is in the first column, you can adjust accordingly
        patient_id = tree.item(selected_item)['values'][0]

        # Open the edit window with the selected patient ID
        self.editWindow = Toplevel(self.newWindow)
        self.editForm = EditPatientForm(self.editWindow, patient_id, self.refresh_view_patients)

    def refresh_view_patients(self):
        # Method to refresh the "View Patients" window
        self.newWindow.destroy()
        self.View_Patients()

    def View_Employees(self):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee")
            employees = cursor.fetchall()

            if not employees:
                messagebox.showinfo("View Employees", "No employees found.")
                return

            self.newWindow = Toplevel(self.master)
            self.newWindow.title("All Employees")
            self.newWindow.geometry("800x600")

            # Create a frame to hold the Treeview and scrollbar
            frame = Frame(self.newWindow)
            frame.pack(expand=True, fill="both")

            tree = ttk.Treeview(frame)
            tree["columns"] = tuple("col" + str(i) for i in range(len(employees[0])))
            tree["show"] = "headings"

            # Change the header names
            header_names = ["Employee ID", "Employee Name", "Sex", "Age", "Designation", "Salary", "Experience", "Email", "Phone"]

            for i, heading in enumerate(header_names):
                tree.heading("col" + str(i), text=heading)
                tree.column("col" + str(i), anchor="center")

            for employee in employees:
                tree.insert("", "end", values=employee)

            tree.pack(side="top", expand=True, fill="both")

            # Add a horizontal scrollbar
            scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            tree.configure(xscrollcommand=scrollbar_x.set)

            edit_button = ttk.Button(self.newWindow, text="Edit", command=lambda: self.edit_employee(tree))
            edit_button.pack(pady=10)

            tree.bind("<Double-1>", lambda event: self.edit_employee(tree))
            delete_button = ttk.Button(self.newWindow, text="Delete", command=lambda: self.delete_employee(tree))
            delete_button.pack(pady=10)

            tree.bind("<Double-1>", lambda event: self.edit_employee(tree))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching employees: {e}")
        finally:
            if cursor:
                cursor.close()

    def delete_employee(self, tree):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Employee", "Please select an employee to delete.")
            return

        # Assuming the employee ID is in the first column, you can adjust accordingly
        employee_id = tree.item(selected_item)['values'][0]

        confirm_delete = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this employee?")
        
        if confirm_delete:
            self.perform_delete_employee(employee_id)
    def perform_delete_employee(self, employee_id):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employee WHERE EMP_ID=?", (employee_id,))
            conn.commit()
            messagebox.showinfo("Success", "Employee deleted successfully!")

            # Refresh the "View Employees" window
            self.refresh_view_employees()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting employee: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_employee(self, tree):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Edit Employee", "Please select an employee to edit.")
            return

        employee_id = tree.item(selected_item)['values'][0]

        self.editWindow = Toplevel(self.newWindow)
        self.editForm = EditEmployeeForm(self.editWindow, employee_id, self.refresh_view_employees)

    def refresh_view_employees(self):
        self.newWindow.destroy()
        self.View_Employees()

    def View_Appointments(self):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointment")
            appointments = cursor.fetchall()

            if not appointments:
                messagebox.showinfo("View Appointments", "No appointments found.")
                return

            self.newWindow = Toplevel(self.master)
            self.newWindow.title("All Appointments")
            self.newWindow.geometry("1200x800")

            tree = ttk.Treeview(self.newWindow)
            tree["columns"] = tuple("col" + str(i) for i in range(len(appointments[0])))
            tree["show"] = "headings"

            header_names = ["Appointment No.", "Patient ID", "Employee ID", "Appointment Date", "Appointment Time"] + [cursor.description[i][0].capitalize() for i in range(5, len(cursor.description))]

            for i, heading in enumerate(header_names):
                tree.heading("col" + str(i), text=heading)
                tree.column("col" + str(i), anchor="center")

            for appointment in appointments:
                tree.insert("", "end", values=appointment)

            tree.pack()

            # Add a horizontal scrollbar
            scrollbar_x = Scrollbar(self.newWindow, orient="horizontal", command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            tree.configure(xscrollcommand=scrollbar_x.set)

            # Add an 'Edit' button
            edit_button = ttk.Button(self.newWindow, text="Edit", command=lambda: self.edit_appointment(tree))
            edit_button.pack(pady=10)

            # Set the background and foreground color of the "Edit" button
            edit_button.configure(style='Custom.TButton', background='lavender', foreground='black')

            # Add a 'Delete' button
            delete_button = ttk.Button(self.newWindow, text="Delete", command=lambda: self.delete_appointment(tree))
            delete_button.pack(pady=10)

            # Set the background and foreground color of the "Delete" button
            delete_button.configure(style='Custom.TButton', background='tomato', foreground='black')

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching appointments: {e}")
        finally:
            if cursor:
                cursor.close()


    def edit_appointment(self, tree):
        # Get the selected item
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Edit Appointment", "Please select an appointment to edit.")
            return

        # Assuming the appointment ID is in the first column, you can adjust accordingly
        appointment_id = tree.item(selected_item)['values'][0]

        # Open the edit window with the selected appointment ID and pass the refresh callback
        self.editWindow = Toplevel(self.newWindow)
        self.editForm = EditAppointmentForm(self.editWindow, appointment_id, self.refresh_view_appointments)

    def delete_appointment(self, tree):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Appointment", "Please select an appointment to delete.")
            return

        # Assuming the appointment ID is in the first column, you can adjust accordingly
        appointment_id = tree.item(selected_item)['values'][0]

        confirm_delete = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this appointment?")

        if confirm_delete:
            self.perform_delete_appointment(appointment_id)

    def perform_delete_appointment(self, appointment_id):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointment WHERE APPOINTMENT_ID=?", (appointment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Appointment deleted successfully!")

            # Refresh the "View Appointments" window
            self.refresh_view_appointments()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting appointment: {e}")
        finally:
            if cursor:
                cursor.close()

    def refresh_view_appointments(self):
        # Method to refresh the "View Appointments" window
        self.newWindow.destroy()
        self.View_Appointments()
    

class LoginPage:
    def __init__(self, master):
        set_custom_style()

        self.master = master
        self.master.title("Login Page")
        self.master.geometry("800x400")
        self.master.config(bg="#E9ECF3")

        left_image = Image.open("manman.jpg")
        left_image = left_image.resize((400, 400), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)

        self.left_image = ImageTk.PhotoImage(left_image)

        self.left_label = tk.Label(self.master, image=self.left_image, bg="#E9ECF3")
        self.left_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.frame = tk.Frame(self.master, bg="#E9ECF3")
        self.frame.place(relx=0.8, rely=0.5, anchor="center", relwidth=0.5, relheight=0.8)

        self.Username = tk.StringVar()
        self.Password = tk.StringVar()

        self.lblTitle = tk.Label(self.frame, text="Login", font="Helvetica 20 bold", bg="#E9ECF3", fg="black")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=20)

        self.AccountName = tk.StringVar()

        self.lblAccountName = tk.Label(self.frame, text="Account Name", font="Helvetica 14 bold", bg="#E9ECF3", fg="black")
        self.lblAccountName.grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.entryAccountName = CustomEntry(self.frame, textvariable=self.AccountName)
        self.entryAccountName.grid(row=3, column=1, pady=10, padx=10, sticky='w')

        self.lblUsername = tk.Label(self.frame, text="Username", font="Helvetica 14 bold", bg="#E9ECF3", fg="black")
        self.lblUsername.grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.entryUsername = CustomEntry(self.frame, textvariable=self.Username)
        self.entryUsername.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        self.lblPassword = tk.Label(self.frame, text="Password", font="Helvetica 14 bold", bg="#E9ECF3", fg="black")
        self.lblPassword.grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.entryPassword = CustomEntry(self.frame, show="*", textvariable=self.Password)
        self.entryPassword.grid(row=2, column=1, pady=10, padx=10, sticky='w')

        self.btnLogin = ttk.Button(self.frame, text="Login", style='Custom.TButton', command=self.login)
        self.btnLogin.grid(row=4, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.Username.get()
        password = self.Password.get()
        account_name = self.AccountName.get()

        if not username or not password:
            tk.messagebox.showerror("Login Failed", "Username and Password are required.")
            return

        # Attempt to login using API first
        try:
            auth_token = self.get_auth_token(username, password, account_name)
            if auth_token:
                self._open_menu(username)
                return
        except Exception as e:
            print(f"API Login failed: {e}. Falling back to local database...")

        # Fallback to local DB login
        try:
            local_conn = database.get_connection()
            cursor = local_conn.cursor()
            combine_user = username + ":" + password
            md5_password = hashlib.md5(combine_user.encode()).hexdigest()
            
            cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, md5_password))
            result = cursor.fetchone()
            
            if result:
                self._open_menu(username)
            else:
                tk.messagebox.showerror("Login Failed", "Invalid username, password, or account name (Local Auth)")
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Database error: {e}")
        finally:
            local_conn.close()

    def _open_menu(self, username):
        self.newWindow = Toplevel(self.master)
        self.app = HospitalMenu(self.newWindow)
        self.master.withdraw()
        print(f"Login successful for {username}")

    def get_auth_token(self, username, password, account_name):
        url = 'https://api.bsnlpbx.com/v2/user_auth'
        headers = {'Content-Type': 'application/json'}
        combine_user = username + ":" + password
        md5_password = hashlib.md5(combine_user.encode()).hexdigest()

        data = {"data": {"credentials": md5_password, "account_name": account_name}}
        
        # Adding a timeout so we don't hang if the API is offline
        response = requests.put(url, headers=headers, json=data, timeout=5)

        if not response.ok:
            raise Exception(f'Failed to update authentication: {response.status_code}')

        json_data = response.json()
        auth_token = json_data.get('auth_token')
        return auth_token

    def Exit(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

