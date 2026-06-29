from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar  # Make sure to have tkcalendar module installed
import sqlite3
from datetime import datetime
import tkinter as tk
import database

# Database connection
conn = database.get_connection()
print("DATABASE CONNECTION SUCCESSFUL")

# Class for booking appointment
class Appointment:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()

        # Attributes
        self.pat_ID = IntVar()
        self.emp_ID = StringVar()
        self.ap_no = StringVar()
        self.ap_time = StringVar()
        self.ap_date = StringVar()
        self.des = StringVar()

        # Title
        self.lblTitle = Label(self.frame, text="APPOINTMENT FORM", font="Helvetica 20 bold", bg="#E9ECF3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        # Frame
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        # Labels
        self.lblpid_label = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblpid_label.grid(row=0, column=0)
        self.lblpid_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.pat_ID)
        self.lblpid_entry.grid(row=0, column=1)
        self.lblpid_entry.delete(0, END)  #

        self.lbldid = Label(self.LoginFrame, text="DOCTOR ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lbldid.grid(row=1, column=0)
        self.lbldid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.emp_ID)
        self.lbldid.grid(row=1, column=1)

        self.lblap = Label(self.LoginFrame, text="APPOINTMENT NO", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblap.grid(row=2, column=0)
        self.lblap = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.ap_no)
        self.lblap.grid(row=2, column=1)

        self.lblapt = Label(self.LoginFrame, text="APPOINTMENT TIME", font="Helvetica 14 bold",
                            bg="#E9ECF3", bd=22)
        self.lblapt.grid(row=0, column=2)
        self.lblapt = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.ap_time)
        self.lblapt.grid(row=0, column=3)

        self.lblapd = Label(self.LoginFrame, text="APPOINTMENT DATE(YYYY-MM-DD)", font="Helvetica 14 bold",
                            bg="#E9ECF3", bd=22)
        self.lblapd.grid(row=1, column=2)
        self.lblapd = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.ap_date)
        self.lblapd.grid(row=1, column=3)
        self.lblapd.bind("<Button-1>", self.open_calendar)  # Bind left mouse click event to open calendar

        self.lbldes = Label(self.LoginFrame, text="DESCRIPTION", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lbldes.grid(row=2, column=2)
        self.lbldes = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.des)
        self.lbldes.grid(row=2, column=3)

        # Buttons
        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.button2 = Button(self.LoginFrame2, text="SAVE", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.INSERT_AP)
        self.button2.grid(row=3, column=1)

        self.button3 = Button(self.LoginFrame2, text="DELETE", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.DE_AP_DISPLAY)
        self.button3.grid(row=3, column=2)

        self.button3 = Button(self.LoginFrame2, text="SEARCH APPOINTMENTS", width=20, font="Helvetica 14 bold",
                              bg="#AF006C", command=self.S_AP_DISPLAY)
        self.button3.grid(row=3, column=3)

        self.button6 = Button(self.LoginFrame2, text="EXIT", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.Exit)
        self.button6.grid(row=3, column=4)

    def Exit(self):
        self.master.destroy()

    def INSERT_AP(self):
        e1 = self.pat_ID.get()
        e2 = self.emp_ID.get()
        e3 = self.ap_no.get()
        e4 = self.ap_time.get()
        e5 = self.ap_date.get()
        e6 = self.des.get()

        p = list(conn.execute("SELECT * FROM appointment WHERE AP_NO =?", (e3,)))
        x = len(p)
        if x != 0:
            tk.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "APPOINTMENT ALREADY EXISTS")
        else:
            conn.execute("Insert into appointment values(?,?,?,?,?,?)", (e1, e2, e3, e4, e5, e6,))
            tk.messagebox.showinfo("Hospital DATABASE SYSTEM", "APPOINTMENT SET SUCCESSFULLY")

            # Clear entry boxes after saving
            self.pat_ID.set('')
            self.emp_ID.set('')
            self.ap_no.set('')
            self.ap_time.set('')
            self.ap_date.set('')
            self.des.set('')

        conn.commit()

    def DE_AP_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = DEL_AP(self.newWindow)

    def S_AP_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = SEA_AP(self.newWindow)

    def open_calendar(self, event):
        top = Toplevel(self.master)
        cal = Calendar(top, font="Arial 14", selectmode="day")
        cal.pack(fill="both", expand=True)

        confirm_btn = Button(top, text="Confirm Date", command=lambda: self.update_date(cal, top))
        confirm_btn.pack()

    def update_date(self, cal, top):
        selected_date = cal.get_date()
        date_obj = datetime.strptime(selected_date, "%m/%d/%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        self.ap_date.set(formatted_date)
        top.destroy()


# Class for delete appointment
class DEL_AP:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()

        self.de1_ap = StringVar()
        self.lblTitle = Label(self.frame, text="DELETE APPOINTMENT WINDOW", font="Helvetica 20 bold", bg="#E9ECF3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame.grid(row=1, column=0)
        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblpatid = Label(self.LoginFrame, text="ENTER APPOINTMENT NO TO DELETE", font="Helvetica 14 bold",
                              bg="#E9ECF3", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.de1_ap)
        self.lblpatid.grid(row=0, column=1)

        self.DeleteB = Button(self.LoginFrame2, text="DELETE", width=10, font="Helvetica 14 bold", bg="#E9ECF3",
                              command=self.DELETE_AP)
        self.DeleteB.grid(row=3, column=1)

    def DELETE_AP(self):
        inp_d = str(self.de1_ap.get())
        v = list(conn.execute("select * from appointment where AP_NO=?", (inp_d,)))
        if len(v) == 0:
            tk.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT APPOINTMENT NOT FIXED")
        else:
            conn.execute('DELETE FROM APPOINTMENT where AP_NO=?', (inp_d,))
            tk.messagebox.showinfo("Hospital DATABASE SYSTEM", "PATIENT APPOINTMENT DELETED")
        conn.commit()


# Class for search appointment
class SEA_AP:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()

        self.entry = StringVar()
        self.lblTitle = Label(self.frame, text="SEARCH APPOINTMENT WINDOW", font="Helvetica 20 bold", bg="#E9ECF3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=25)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame.grid(row=1, column=0)
        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblpatid = Label(self.LoginFrame, text="ENTER DATE TO VIEW APPOINTMENTS(YYYY-MM-DD)",
                              font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.entry)
        self.lblpatid.grid(row=0, column=1)

        self.SearchB = Button(self.LoginFrame2, text="SEARCH", width=10, font="Helvetica 14 bold", bg="#E9ECF3",
                              command=self.SEARCH_AP)
        self.SearchB.grid(row=0, column=1)

    def SEARCH_AP(self):
        ap = self.entry.get()
        c1 = conn.cursor()
        p = list(c1.execute("select * from appointment where AP_DATE=?", (ap,)))
        if len(p) == 0:
            tk.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "THERE'S NO APPOINTMENT BOOKED")
        else:
            t = c1.execute(
                'SELECT PATIENT_ID,NAME,AP_NO,EMP_ID,AP_DATE,AP_TIME FROM PATIENT NATURAL JOIN appointment where AP_DATE=?',
                (ap,))
            for i in t:
                l1 = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                l1.grid(row=1, column=0)
                dis1 = Label(self.LoginFrame, font="Helvetica 14 bold", bd=2, bg="#E9ECF3", text=i[0])
                dis1.grid(row=1, column=1)
                l2 = Label(self.LoginFrame, text="PATIENT NAME", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                l2.grid(row=2, column=0)
                dis2 = Label(self.LoginFrame, font="Helvetica 14 bold", bd=2, bg="#E9ECF3", text=i[1])
                dis2.grid(row=2, column=1)

                l3 = Label(self.LoginFrame, text="APPOINTMENT NO", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                l3.grid(row=3, column=0)
                dis3 = Label(self.LoginFrame, font="Helvetica 14 bold", bg="#E9ECF3", bd=2, text=i[2])
                dis3.grid(row=3, column=1)

                l4 = Label(self.LoginFrame, text="DOCTOR ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                l4.grid(row=4, column=0)
                dis4 = Label(self.LoginFrame, font="Helvetica 14 bold", bg="#E9ECF3", bd=2, text=i[3])
                dis4.grid(row=4, column=1)

                l5 = Label(self.LoginFrame, text="APPOINTMENT TIME(HH:MM:SS)", font="Helvetica 14 bold", bg="#E9ECF3",
                           bd=22)
                l5.grid(row=5, column=0)
                dis5 = Label(self.LoginFrame, font="Helvetica 14 bold", bg="#E9ECF3", bd=2, text=i[5])
                dis5.grid(row=5, column=1)



