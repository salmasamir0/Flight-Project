import tkinter
import sqlite3
from tkinter import messagebox
from edit_reservations import update_delete_page

def open_reservations_page(window):
    global reservations_list, reservations_window, reservations_label, search_results, scrollbar,load_data
    print("I am working....")
    reservations_window = tkinter.Toplevel(window)
    reservations_window.title("Reservation Page")
    reservations_window.geometry("600x500")

    reservations_label = tkinter.Label(reservations_window, text="All Reservations", font=("Times New Roman",20,"bold"), fg="Red")
    reservations_label.pack(pady=5, anchor="center")

    frame = tkinter.Frame(reservations_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)   

    reservations_list = tkinter.Listbox(frame, width=60, height=15)
    reservations_list.pack(side="left", expand=True, fill="both")
    
    scrollbar = tkinter.Scrollbar(frame, orient="vertical", command=reservations_list.yview)
    scrollbar.pack(side="right", fill="y")
    reservations_list.config(yscrollcommand=scrollbar.set)

    search_results = tkinter.Label(reservations_window, text="", fg="grey")
    search_results.pack(pady=5)

    # دالة تحميل البيانات
    def load_data():
        reservations_list.delete(0, tkinter.END)
        
        try:
            conn = sqlite3.connect("flights.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, flight_number, seat_number, departure, destination, date FROM reservations ORDER BY id ASC")
            rows = cursor.fetchall()
            print(rows)
            conn.commit()
            conn.close()

            if not rows:
                search_results.config(text="No Results!!")
            else:
                search_results.config(text=f"{len(rows)} reservation(s) found")
                for rid, name, flight_number, seat_number, departure, destination, date in rows:
                    reservations_list.insert(tkinter.END,
                                             f"{rid} | name: {name} | Flight no.: {flight_number} | Seat no.: {seat_number} | Departure: {departure} | Final Destination: {destination} | Flight Date: {date}") 
                    

        except Exception as e:
            messagebox.showerror("ERROR", f"Can't show reservations.\n{e}")

    # Refresh
    refresh_button = tkinter.Button(reservations_window, text="Refresh", command=load_data, font=("Ariel",14,"bold"), fg="White", bg="Red")
    refresh_button.pack(pady=5)
 
    def selected_for_edit():
        selected = reservations_list.curselection()
        if not selected:
            return  # لو مفيش اختيار، ما يعملش حاجة

        selected_text = reservations_list.get(selected[0])
        rid = int(selected_text.split("|")[0].strip())
        name = selected_text.split("name: ")[1].split("|")[0].strip()
        flight_number  = selected_text.split("Flight no.:")[1].split("|")[0].strip()
        seat_number = selected_text.split("Seat no.: ")[1].split("|")[0].strip()
        departure = selected_text.split("Departure: ")[1].split("|")[0].strip()
        destination = selected_text.split("Final Destination: ")[1].split("|")[0].strip()
        date = selected_text.split("Flight Date: ")[1].strip()
        
        update_delete_page(reservations_window, rid, name, flight_number, seat_number, departure, destination, date, load_data)

    update_delete_button = tkinter.Button(reservations_window, text="Update / Delete Selected",
                                         font=("Ariel",14,"bold"), fg="white", bg="blue",
                                         command=selected_for_edit)
    update_delete_button.pack(pady=10)

    load_data()