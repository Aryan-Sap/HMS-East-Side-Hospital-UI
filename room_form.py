from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import requests
import database
    base_url = "https://api.agify.io"
    endpoint = "/"

    params = {
        "name": name,
        "country_id": country_id
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

name = "michael"
country_id = "US"

try:
    agify_data = get_agify_data(name, country_id)

    if agify_data:
        print("Agify data:")
        print(agify_data)
    else:
        print("Failed to retrieve Agify data.")
except Exception as e:
    print(f"Agify error: {e}")

conn = database.get_connection()

class Room:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()

        self.P_id = IntVar(value='')
        self.room_t = StringVar(value='')
        self.room_no = StringVar(value='')
        self.rate = IntVar(value="")
        self.da = StringVar(value='')
        self.dd = StringVar(value='')

        self.lblTitle = Label(self.frame, text="ROOM ALLOCATION FORM", font="Helvetica 20 bold", bg="#E9ECF3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblpatid = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.P_id)
        self.lblpatid.grid(row=0, column=1)

        self.room_t1 = Label(self.LoginFrame, text="ROOM TYPE", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.room_t1.grid(row=1, column=0)
        self.room_t1 = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.room_t)
        self.room_t1.grid(row=1, column=1)

        self.room_no1 = Label(self.LoginFrame, text="ROOM NUMBER ", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.room_no1.grid(row=2, column=0)
        self.room_no1 = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.room_no)
        self.room_no1.grid(row=2, column=1)

        self.lblrate = Label(self.LoginFrame, text="ROOM CHARGES", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblrate.grid(row=0, column=2)
        self.lblrate = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.rate)
        self.lblrate.grid(row=0, column=3)

        self.lblda = Label(self.LoginFrame, text="DATE ADMITTED", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblda.grid(row=1, column=2)
        self.cal_admitted = DateEntry(self.LoginFrame, font="Helvetica 14 bold", bd=2)
        self.cal_admitted.grid(row=1, column=3)

        self.lbldd = Label(self.LoginFrame, text="DATE DISCHARGED", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lbldd.grid(row=2, column=2)
        self.cal_discharged = DateEntry(self.LoginFrame, font="Helvetica 14 bold", bd=2, validate="focusout", validatecommand=self.validate_dates)
        self.cal_discharged.grid(row=2, column=3)

        self.button2 = Button(self.LoginFrame2, text="SUBMIT", width=10, font="Helvetica 14 bold", bg="#AF006C", command=self.INSERT_ROOM)
        self.button2.grid(row=3, column=1)

        self.button3 = Button(self.LoginFrame2, text="UPDATE", width=10, font="Helvetica 14 bold", bg="#AF006C", command=self.UPDATE_ROOM)
        self.button3.grid(row=3, column=2)

        self.button5 = Button(self.LoginFrame2, text="ROOM DETAILS", width=15, font="Helvetica 14 bold", bg="#AF006C", command=self.SEARCH_ROOM)
        self.button5.grid(row=3, column=4)

        self.button6 = Button(self.LoginFrame2, text="EXIT", width=10, font="Helvetica 14 bold", bg="#AF006C", command=self.Exit)
        self.button6.grid(row=3, column=5)

        room_type_options = ["Single Room: Rs 4500", "Twin Sharing: Rs 2500", "Triple Sharing: Rs 2000"]
        self.room_type_var = StringVar()
        self.room_type_var.set(room_type_options[0])

        self.room_type_dropdown = ttk.Combobox(self.LoginFrame, textvariable=self.room_type_var,
                                               values=room_type_options, font="Helvetica 14 bold", state='readonly')
        self.room_type_dropdown.grid(row=1, column=1)
        self.room_type_dropdown.bind("<Button-1>", self.open_dropdown)

    def open_dropdown(self, event):
        self.room_type_dropdown.event_generate('<Down>', when='tail')

    def validate_dates(self):
        date_admitted = self.cal_admitted.get_date()
        date_discharged = self.cal_discharged.get_date()

        if date_admitted is not None and date_discharged is not None:
            if date_discharged < date_admitted:
                tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "DATE DISCHARGED cannot be before DATE ADMITTED")
                return False
        return True

    def INSERT_ROOM(self):
        global r1, r2, r3, r4, r5, r6, conn, p
        conn = database.get_connection()
        conn.cursor()
        r1 = (self.P_id.get())
        r2 = (self.room_t.get())
        r3 = (self.room_no.get())
        r4 = (self.rate.get())
        r5 = (self.cal_admitted.get_date())
        r6 = (self.cal_discharged.get_date())
        p = list(conn.execute("SELECT * FROM ROOM WHERE ROOM_NO=?", (r3,)))
        x = len(p)
        if x != 0:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "ROOM_NO IS CURRENTLY OCCUPIED")
        else:
            conn.execute('INSERT INTO ROOM VALUES(?,?,?,?,?,?)', (r1, r3, r2, r4, r5, r6,))
            tkinter.messagebox.showinfo("HOSPITAL DATABSE SYSTEM", "ROOM ALLOCATED")
            conn.commit()

    def SEARCH_ROOM(self):
        self.newWindow = Toplevel(self.master)
        self.app = S_Room(self.newWindow)

    def Exit(self):
        self.master.destroy()

    def UPDATE_ROOM(self):
        global r1, r2, room_t, da, dd, rate, room_no, r3, r4, r5, r6, conn
        r1 = (self.P_id.get())
        r2 = (self.room_t.get())
        r3 = (self.room_no.get())
        r4 = (self.rate.get())
        r5 = (self.cal_admitted.get_date())
        r6 = (self.cal_discharged.get_date())
        p = list(conn.execute("Select * from ROOM where PATIENT_ID=? AND ROOM_NO=?", (r1, r3,)))
        if len(p) != 0:
            tkinter.messagebox.showerror("HOSPITAL DATABSE SYSTEM", "PATIENT IS NOT ALLOCATED A ROOM")
        else:
            conn.execute('UPDATE ROOM SET ROOM_NO=?,ROOM_TYPE=?,RATE=?,DATE_ADMITTED=?,DATE_DISCHARGED=? where PATIENT_ID=?', (r3, r2, r4, r5, r6, r1,))
            tkinter.messagebox.showinfo("HOSPITAL DATABSE SYSTEM", "ROOM DETAILS UPDATED")
            conn.commit()


class S_Room:
    def __init__(self, master):
        global inp_s, entry, SearchB
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#E9ECF3")
        self.frame = Frame(self.master, bg="#E9ECF3")
        self.frame.pack()
        self.Pr_id = IntVar()
        self.lblTitle = Label(self.frame, text="SEARCH PATIENT DETAILS", font="Helvetica 20 bold", bg="#E9ECF3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=25)

        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame.grid(row=1, column=0)
        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#E9ECF3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblpatid = Label(self.LoginFrame, text="ENTER PATIENT ID TO SEARCH", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.Pr_id)
        self.lblpatid.grid(row=0, column=1)

        self.SearchB = Button(self.LoginFrame2, text="SEARCH", width=10, font="Helvetica 14 bold", bg="#E9ECF3", command=self.ROOM_DISPLAY)
        self.SearchB.grid(row=0, column=1)

    def ROOM_DISPLAY(self):
        global pat_rm, lr1, dis1, lr2, dis2, c1, i, conn, Pr_id
        conn = database.get_connection()
        c1 = conn.cursor()
        pat_rm = (self.Pr_id.get())
        p = list(c1.execute('select * from  ROOM  where PATIENT_ID=?', (pat_rm,)))
        if (len(p) == 0):
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT NOT ALLOCATED ROOM")
        else:
            t = c1.execute('SELECT PATIENT_ID,NAME,ROOM_NO,ROOM_TYPE FROM ROOM NATURAL JOIN PATIENT where PATIENT_ID=?', (pat_rm,))
            for i in t:
                self.l1 = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                self.l1.grid(row=1, column=0)
                self.dis1 = Label(self.LoginFrame, font="Helvetica 14 bold", bd=2, bg="#E9ECF3", text=i[0])
                self.dis1.grid(row=1, column=1)

                self.l2 = Label(self.LoginFrame, text="PATIENT NAME", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                self.l2.grid(row=2, column=0)
                self.dis2 = Label(self.LoginFrame, font="Helvetica 14 bold", bd=2, bg="#E9ECF3", text=i[1])
                self.dis2.grid(row=2, column=1)

                self.l3 = Label(self.LoginFrame, text="ROOM NO", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                self.l3.grid(row=1, column=2)
                self.dis3 = Label(self.LoginFrame, font="Helvetica 14 bold", bg="#E9ECF3", bd=2, text=i[2])
                self.dis3.grid(row=1, column=3)

                self.l4 = Label(self.LoginFrame, text="ROOM TYPE", font="Helvetica 14 bold", bg="#E9ECF3", bd=22)
                self.l4.grid(row=2, column=2)
                self.dis4 = Label(self.LoginFrame, font="Helvetica 14 bold", bg="#E9ECF3", bd=2, text=i[3])
                self.dis4.grid(row=2, column=3)

