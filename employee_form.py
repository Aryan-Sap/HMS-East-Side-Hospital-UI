from tkinter import *
import tkinter.messagebox
import sqlite3
from tkinter import ttk

conn = sqlite3.connect("HospitalDB.db")
print("DATABASE CONNECTION SUCCESSFUL")

class Employee:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#d3d3d3")
        self.frame = Frame(self.master, bg="#d3d3d3")
        self.frame.pack()

        self.emp_ID = StringVar()
        self.emp_name = StringVar()
        self.emp_sex = StringVar()
        self.emp_age = StringVar(value="")
        self.emp_type = StringVar()
        self.emp_salary = StringVar(value="")
        self.emp_exp = StringVar()
        self.emp_email = StringVar()
        self.emp_phno = StringVar(value="")

        self.lblTitle = Label(self.frame, text="EMPLOYEE REGISTRATION FORM", font="Helvetica 20 bold", bg="#d3d3d3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#d3d3d3", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#d3d3d3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblempid = Label(self.LoginFrame, text="EMPLOYEE ID", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblempid.grid(row=0, column=0)
        self.lblempid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_ID)
        self.lblempid.grid(row=0, column=1)

        self.lblempname = Label(self.LoginFrame, text="EMPLOYEE NAME", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblempname.grid(row=1, column=0)
        self.lblempname = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_name)
        self.lblempname.grid(row=1, column=1)

        self.lblsex = Label(self.LoginFrame, text="SEX", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblsex.grid(row=2, column=0)

        sex_options = ["Male", "Female", "Other"]
        self.sex_var = StringVar()
        self.sex_var.set(sex_options[0])  # Set default value

        self.sex_dropdown = ttk.Combobox(self.LoginFrame, textvariable=self.sex_var, values=sex_options,
                                         font="Helvetica 14 bold", state='readonly')
        self.sex_dropdown.grid(row=2, column=1)

        self.lblage = Label(self.LoginFrame, text="AGE", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblage.grid(row=3, column=0)
        self.lblage = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_age)
        self.lblage.grid(row=3, column=1)

        self.etype1 = Label(self.LoginFrame, text="EMPLOYEE DESIGNATION", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.etype1.grid(row=4, column=0)
        self.etype1 = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_type)
        self.etype1.grid(row=4, column=1)

        self.lblCon = Label(self.LoginFrame, text="SALARY", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblCon.grid(row=0, column=2)
        self.lblCon = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_salary)
        self.lblCon.grid(row=0, column=3)

        self.lblAlt = Label(self.LoginFrame, text="EXPERIENCE", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblAlt.grid(row=1, column=2)
        self.lblAlt = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_exp)
        self.lblAlt.grid(row=1, column=3)

        self.lbleid = Label(self.LoginFrame, text="CONTACT NUMBER", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lbleid.grid(row=2, column=2)
        self.lbleid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_phno)
        self.lbleid.grid(row=2, column=3)

        self.lbleid = Label(self.LoginFrame, text="EMAIL", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lbleid.grid(row=3, column=2)
        self.lbleid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_email)
        self.lbleid.grid(row=3, column=3)

        self.button2 = Button(self.LoginFrame2, text="SAVE", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.INSERT_EMP)
        self.button2.grid(row=3, column=1)

        self.button6 = Button(self.LoginFrame2, text="EXIT", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.Exit)
        self.button6.grid(row=3, column=3)
        self.lblempid = Label(self.LoginFrame, text="EMPLOYEE ID", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblempid.grid(row=0, column=0)
        self.lblempid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_ID)
        self.lblempid.grid(row=0, column=1)
        self.lblAlt = Label(self.LoginFrame, text="EXPERIENCE(in years)", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblAlt.grid(row=1, column=2)
        self.lblAlt = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_exp)
        self.lblAlt.grid(row=1, column=3)

        # Adding validation to allow only numbers and symbols for EXPERIENCE
        self.lblAlt.config(validate="key", validatecommand=(self.lblAlt.register(self.validate_experience_input), "%P"))

        # Adding validation to allow only numerical input for EMPLOYEE ID
        self.lblempid.config(validate="key", validatecommand=(self.lblempid.register(self.validate_numeric_input), "%P"))
    def validate_numeric_input(self, new_value):
        try:
            # Check if the new value can be converted to an integer
            int(new_value)
            return True
        except ValueError:
            # If not, show an error message and reject the input
            tkinter.messagebox.showerror("Invalid Input", "Please enter numerical values only.")
            return False
    def validate_experience_input(self, new_value):
        # Check if the new value contains only numbers and symbols
        if any(c.isalpha() for c in new_value):
            tkinter.messagebox.showerror("Invalid Input", "Please enter numbers and symbols only for EXPERIENCE.")
            return False
        return True
    def Exit(self):
        self.master.destroy()

    def INSERT_EMP(self):
        global e1, e2, e3, e4, e5, e6, e7, e8, e9, var
        e1 = (self.emp_ID.get())
        e2 = (self.emp_name.get())
        e3 = (self.sex_var.get())  # Get the selected value from the dropdown
        e4 = (self.emp_age.get())
        e5 = (self.emp_type.get())
        e6 = (self.emp_salary.get())
        e7 = (self.emp_exp.get())
        e8 = (self.emp_email.get())
        e9 = (self.emp_phno.get())

        # Validation to check if any field is empty
        if not all([e1, e2, e3, e4, e5, e6, e7, e8, e9]):
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "Please fill in all the fields")

            # Change the background color of empty entry boxes to red
            for entry_widget in [self.lblempid, self.lblempname, self.lblage, self.etype1, self.lblCon, self.lblAlt,
                                 self.lbleid, self.lbleid, self.lbleid]:
                if not entry_widget.get():
                    entry_widget.config(bg="#FF7F7F")
            return

        conn = sqlite3.connect("HospitalDB.db")
        p = list(conn.execute("SELECT * FROM employee  WHERE EMP_ID =?", (e1,)))
        x = len(p)
        if x != 0:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "EMPLOYEE ID ALREADY EXISTS")
        else:
            conn.execute("INSERT INTO employee VALUES(?,?,?,?,?,?,?,?,?)", (e1, e2, e3, e4, e5, e6, e7, e8, e9,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "Employee added successfully")
        conn.commit()


