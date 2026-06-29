from tkinter import *
import tkinter.messagebox
import sqlite3
from tkcalendar import DateEntry

# Class for BILLING
class Billing:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="#d3d3d3")
        self.frame = Frame(self.master, bg="#d3d3d3")
        self.frame.pack()

        # ==============ATTRIBUTES===========
        self.P_id = StringVar()
        self.dd = StringVar()
        self.treat_1 = StringVar()
        self.treat_2 = StringVar()
        self.cost_t = StringVar()
        self.med = StringVar()
        self.med_q = StringVar()
        self.price = StringVar()
        self.room_number = StringVar()
        self.room_price = StringVar()

        # ===============TITLE==========
        self.lblTitle = Label(self.frame, text="BILLING WINDOW", font="Helvetica 20 bold", bg="#d3d3d3")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=25)

        # ==============FRAME==========
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="#d3d3d3", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="#d3d3d3", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        # ===========LABELS=============
        self.total_sum_label = Label(self.LoginFrame, text="TOTAL AMOUNT OUTSTANDING", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.total_sum_label.grid(row=6, column=0)

        self.total_sum_value = Label(self.LoginFrame, text="", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.total_sum_value.grid(row=6, column=1)
        self.lblpid = Label(self.LoginFrame, text="PATIENT ID", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblpid.grid(row=0, column=0)
        self.lblpid_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.P_id)
        self.lblpid_entry.grid(row=0, column=1)

        self.lbldid = Label(self.LoginFrame, text="DATE DISCHARGED", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lbldid.grid(row=1, column=0)
        self.lbldid_entry = DateEntry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.dd, date_pattern="yyyy-mm-dd")
        self.lbldid_entry.grid(row=1, column=1)

        self.lbltreat = Label(self.LoginFrame, text="TREATMENT", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lbltreat.grid(row=2, column=0)
        self.lbltreat_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.treat_1)
        self.lbltreat_entry.grid(row=2, column=1)

        self.lblcode_t1 = Label(self.LoginFrame, text="TREATMENT CODE", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblcode_t1.grid(row=3, column=0)
        self.lblcode_t1_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.treat_2)
        self.lblcode_t1_entry.grid(row=3, column=1)

        self.lblap = Label(self.LoginFrame, text="TREATMENT COST ₹", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblap.grid(row=4, column=0)
        self.lblap_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.cost_t)
        self.lblap_entry.grid(row=4, column=1)

        self.lblmed = Label(self.LoginFrame, text="MEDICINE", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblmed.grid(row=2, column=2)
        self.lblmed_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.med)
        self.lblmed_entry.grid(row=2, column=3)

        self.med_t1 = Label(self.LoginFrame, text="MEDICINE QUANTITY", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.med_t1.grid(row=3, column=2)
        self.med_t1_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.med_q)
        self.med_t1_entry.grid(row=3, column=3)

        self.lblapd = Label(self.LoginFrame, text="MEDICINE PRICE ₹", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblapd.grid(row=4, column=2)
        self.lblapd_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.price)
        self.lblapd_entry.grid(row=4, column=3)

        # ===========LABELS FOR ROOM DETAILS=============
        self.lblroom = Label(self.LoginFrame, text="ROOM NUMBER", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblroom.grid(row=5, column=2)
        self.lblroom_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.room_number)
        self.lblroom_entry.grid(row=5, column=3)

        self.lblprice = Label(self.LoginFrame, text="ROOM PRICE ₹", font="Helvetica 14 bold", bg="#d3d3d3", bd=22)
        self.lblprice.grid(row=5, column=4)
        self.lblprice_entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.room_price)
        self.lblprice_entry.grid(row=5, column=5)

        # ... (Your existing code)

        # ===========BUTTONS=============
        self.button3 = Button(self.LoginFrame2, text="UPDATE DATA", width=15, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.UPDATE_DATA)
        self.button3.grid(row=3, column=2)

        self.button3 = Button(self.LoginFrame2, text="GENERATE BILL", width=15, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.GEN_BILL)
        self.button3.grid(row=3, column=3)

        self.button6 = Button(self.LoginFrame2, text="EXIT", width=10, font="Helvetica 14 bold", bg="#AF006C",
                              command=self.Exit)
        self.button6.grid(row=3, column=4)

        # ... (Your existing code)

    # FUNCTION TO UPDATE DATE IN BILLING FORM
    def UPDATE_DATA(self):
        global c1, b1, P_id, b3, b4, b5, b6, dd, treat_1, treat_2, cost_t, b7, b8, med, med_q, price, u
        conn = sqlite3.connect("HospitalDB.db")
        c1 = conn.cursor()
        b1 = (self.P_id.get())
        b3 = (self.treat_1.get())
        b4 = (self.treat_2.get())
        b5 = (self.cost_t.get())
        b6 = (self.med.get())
        b7 = (self.med_q.get())
        b8 = (self.price.get())
         # Fetch room details based on the patient ID
        room_details = list(conn.execute("SELECT ROOM_NO, RATE FROM room WHERE PATIENT_ID=?", (b1,)))
        if len(room_details) != 0:
            room_number, room_price = room_details[0]
            self.room_number.set(room_number)
            self.room_price.set(room_price)
        else:
            # No room allocated, set ROOM NUMBER and ROOM PRICE to None
            self.room_number.set("None")
            self.room_price.set("None")
        # Fetch room details based on the patient ID
        room_details = list(conn.execute("SELECT ROOM_NO, RATE FROM room WHERE PATIENT_ID=?", (b1,)))
        if len(room_details) != 0:
            room_number, room_price = room_details[0]
            self.room_number.set(room_number)
            self.room_price.set(room_price)

        # ... (Your existing code)

    # FUNCTION TO GENERATE BILL IN BILLING FORM
    def GEN_BILL(self):
        global b1
        b1 = (self.P_id.get())
        conn = sqlite3.connect("HospitalDB.db")

        # Fetching the treatment cost
        treatment_cost = int(self.lblap_entry.get())

        # Fetching the medicine price
        medicine_price = int(self.lblapd_entry.get())

        # Checking if the patient has a room
        room_details = conn.execute("SELECT sum(RATE) FROM ROOM WHERE PATIENT_ID=?", (b1,)).fetchone()
        
        if room_details and room_details[0] is not None:
            # If room is assigned and has a price, use the room price
            room_price = room_details[0]
        else:
            # If no room is assigned or room price is None, set room_price to 0
            room_price = 0

        # Calculating the total sum
        total_cost = treatment_cost + medicine_price + room_price

        # Updating the total sum label
        self.total_sum_value.config(text=total_cost)

    # FUNCTION TO EXIT BILLING WINDOW
    def Exit(self):
        self.master.destroy()

