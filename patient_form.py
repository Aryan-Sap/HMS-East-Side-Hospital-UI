from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry

conn = sqlite3.connect("HospitalDB.db")
print("DATABASE CONNECTION SUCCESSFUL")

# Class for PATIENT REGISTRATION
class Patient:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#d3d3d3")
        self.frame = Frame(self.master, bg="#d3d3d3")
        self.frame.pack()

        # =============ATTRIBUTES===========
        self.pat_ID = StringVar()  # Change IntVar() to StringVar()
        self.pat_name = StringVar()
        self.pat_dob = StringVar()
        self.pat_address = StringVar()
        self.pat_sex = StringVar()
        self.pat_BG = StringVar()
        self.pat_email = StringVar()
        self.pat_contact = StringVar()  # Change IntVar() to StringVar()
        self.pat_contactalt = StringVar()  # Change IntVar() to StringVar()
        self.pat_CT = StringVar()

        # ===============TITLE==========
        self.lblTitle = Label(self.frame, text="PATIENT REGISTRATION FORM", font="Helvetica 20 bold", fg="black",
                              bg="#d3d3d3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)
        # ==============FRAME==========
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#d3d3d3", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        # ===========LABELS=============
        self.lblpatid = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", fg="black", bg="#d3d3d3",
                              bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_ID)
        self.lblpatid.grid(row=0, column=1)

        self.lblPatname = Label(self.LoginFrame, text="PATIENT NAME", font="Helvetica 14 bold", fg="black",
                                bg="#d3d3d3", bd=22)
        self.lblPatname.grid(row=1, column=0)
        self.lblPatname = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_name)
        self.lblPatname.grid(row=1, column=1)

        self.lblsex = Label(self.LoginFrame, text="SEX", font="Helvetica 14 bold", fg="black", bg="#d3d3d3", bd=22)
        self.lblsex.grid(row=2, column=0)
        self.lblsex = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_sex)
        self.lblsex.grid(row=2, column=1)

        self.lblDOB = Label(self.LoginFrame, text="DOB (YYYY-MM-DD)", font="Helvetica 14 bold", fg="black",
                            bg="#d3d3d3", bd=22)
        self.lblDOB.grid(row=3, column=0)
        
        # Use DateEntry widget for the DOB entry
        self.dob_entry = DateEntry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_dob,
                                   date_pattern='yyyy-mm-dd')
        self.dob_entry.grid(row=3, column=1)

        self.lblbgrp = Label(self.LoginFrame, text="BLOOD GROUP", font="Helvetica 14 bold", fg="black", bg="#d3d3d3",
                             bd=22)
        self.lblbgrp.grid(row=4, column=0)

        # Dropdown for Blood Group
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.lblbgrp = ttk.Combobox(self.LoginFrame, font="Helvetica 14 bold", textvariable=self.pat_BG, values=blood_groups)
        self.lblbgrp.grid(row=4, column=1)

        self.lblCon = Label(self.LoginFrame, text="CONTACT NUMBER", font="Helvetica 14 bold", fg="black",
                            bg="#d3d3d3", bd=22)
        self.lblCon.grid(row=0, column=2)
        self.lblCon = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_contact)
        self.lblCon.grid(row=0, column=3)

        self.lblAlt = Label(self.LoginFrame, text="ALTERNATE CONTACT", font="Helvetica 14 bold", fg="black",
                            bg="#d3d3d3", bd=22)
        self.lblAlt.grid(row=1, column=2)
        self.lblAlt = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_contactalt)
        self.lblAlt.grid(row=1, column=3)

        self.lbleid = Label(self.LoginFrame, text="EMAIL", font="Helvetica 14 bold", fg="black", bg="#d3d3d3", bd=22)
        self.lbleid.grid(row=2, column=2)
        self.lbleid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_email)
        self.lbleid.grid(row=2, column=3)

        self.lbldoc = Label(self.LoginFrame, text="CONSULTING TEAM / DOCTOR", font="Helvetica 14 bold", fg="black",
                            bg="#d3d3d3", bd=22)
        self.lbldoc.grid(row=3, column=2)
        self.lbldoc = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_CT)
        self.lbldoc.grid(row=3, column=3)

        self.lbladd = Label(self.LoginFrame, text="ADDRESS", font="Helvetica 14 bold", fg="black", bg="#d3d3d3", bd=22)
        self.lbladd.grid(row=4, column=2)
        self.lbladd = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_address)
        self.lbladd.grid(row=4, column=3)
        

        # ===========BUTTONS=============
        self.button2 = Button(self.LoginFrame, text="SUBMIT", width=10, font="Helvetica 14 bold", fg="black",
                              bg="#AF006C", command=self.INSERT_PAT)
        self.button2.grid(row=5, column=1, pady=20)
        self.button_exit = Button(self.LoginFrame, text="EXIT", width=10, font="Helvetica 14 bold", fg="black",
                                  bg="#AF006C", command=self.Exit)
        self.button_exit.grid(row=5, column=2, pady=20)
        # Dropdown for Sex
        self.lblsex = Label(self.LoginFrame, text="SEX", font="Helvetica 14 bold", fg="black", bg="#d3d3d3", bd=22)
        self.lblsex.grid(row=2, column=0)

        sex_options = ["Male", "Female", "Other"]
        self.sex_var = StringVar()
        self.sex_var.set(sex_options[0])  # Set default value

        self.sex_dropdown = ttk.Combobox(self.LoginFrame, textvariable=self.sex_var, values=sex_options,
                                         font="Helvetica 14 bold", state='readonly')
        self.sex_dropdown.grid(row=2, column=1)

        # ... (remaining code)

    def update_sex_entry(self, value):
        # Update the readonly entry when the dropdown selection changes
        self.sex_var.set(value)

    def INSERT_PAT(self):
        global pp1, pp2, pp3, pp4, pp5, pp6, pp7, pp8, pp9, pp10, ce1, conn
        conn.cursor()
        if not all([self.pat_ID.get(), self.pat_name.get(), self.pat_sex.get(), self.pat_BG.get(),
                    self.pat_dob.get(), self.pat_contact.get(), self.pat_contactalt.get(),
                    self.pat_address.get(), self.pat_CT.get(), self.pat_email.get()]):
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "Please fill in all the fields.")
            # Change the background color of empty entry boxes to red
            for entry_widget in [self.lblpatid, self.lblPatname, self.lblsex, self.dob_entry, self.lblbgrp,
                                 self.lblCon, self.lblAlt, self.lbleid, self.lbldoc, self.lbladd]:
                if not entry_widget.get():
                    entry_widget.config(bg="#FF7F7F")
            return

        # Continue with the insertion if all fields are filled
        p1 = self.pat_ID.get()
        p2 = self.pat_name.get()
        p3 = self.pat_sex.get()
        p4 = self.pat_BG.get()
        p5 = self.pat_dob.get()
        p6 = self.pat_contact.get()
        p7 = self.pat_contactalt.get()
        p8 = self.pat_address.get()
        p9 = self.pat_CT.get()
        p10 = self.pat_email.get()

        p = list(conn.execute("SELECT * FROM PATIENT  WHERE PATIENT_ID =?", (p1,)))
        x = len(p)
        if x != 0:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT_ID ALREADY EXISTS")
        else:
            conn.execute('INSERT INTO PATIENT VALUES(?,?,?,?,?,?,?,?)', (p1, p2, p3, p4, p5, p8, p9, p10,))
            conn.execute('INSERT INTO CONTACT_NO VALUES (?,?,?)', (p1, p6, p7,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "DETAILS INSERTED INTO DATABASE")
        conn.commit()
        p1 = (self.pat_ID.get())
        p2 = (self.pat_name.get())
        p3 = (self.pat_sex.get())
        p4 = (self.pat_BG.get())
        p5 = (self.pat_dob.get())
        p6 = (self.pat_contact.get())
        p7 = (self.pat_contactalt.get())
        p8 = (self.pat_address.get())
        p9 = (self.pat_CT.get())
        p10 = (self.pat_email.get())
        p = list(conn.execute("SELECT * FROM PATIENT  WHERE PATIENT_ID =?", (p1,)))
        x = len(p)
        if x != 0:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT_ID ALREADY EXISTS")
        else:
            conn.execute('INSERT INTO PATIENT VALUES(?,?,?,?,?,?,?,?)', (p1, p2, p3, p4, p5, p8, p9, p10,))
            conn.execute('INSERT INTO CONTACT_NO VALUES (?,?,?)', (p1, p6, p7,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "DETAILS INSERTED INTO DATABASE")
        conn.commit()


    def Exit(self):
        self.master.destroy()


