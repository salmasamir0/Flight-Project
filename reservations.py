import tkinter
import dataBase 
import sqlite3
from edit_reservations import update_delete_page
from tkinter import messagebox

def open_reservations_page(window):
    print("i am working...") 
    global reservations_list, reservations_window, reservations_label, search_results, scrollbar, load_data

    reservations_window = tkinter.Toplevel(window)
    reservations_window.title("Reservation Page")
    reservations_window.geometry("400x400")

    reservations_label = tkinter.Label(reservations_window, text="All Reservations", font=("Times New Roman",20,"bold"),fg="Red")
    reservations_label.pack(pady=5, anchor="center")

    frame = tkinter.Frame(reservations_window)
    frame.pack(fill="both", expand="True", padx=10, pady=10, )   

    reservations_list = tkinter.Listbox(frame,width=60, height=15)
    reservations_list.pack(side="left", expand="True", fill="both")
    
    scrollbar = tkinter.Scrollbar(frame, orient="vertical", command=reservations_list.yview)
    scrollbar.pack(side="right", fill="y")
    reservations_list.config(yscrollcommand=scrollbar.set)

    search_results = tkinter.Label(reservations_window, text="", fg="grey")
    search_results.pack(pady=5)
    
    def load_data():
        reservations_list.delete(0,tkinter.END)
        
        try: 
            conn = sqlite3.connect("flights.db")
            cursor = conn.cursor()
            cursor.execute(""" SELECT id,name,flight_number,seat_number,departure,destination,date
                            FROM reservations
                            ORDER BY id ASC
                            """)
            rows = cursor.fetchall()
            print(rows)
            conn.commit()
            conn.close()

            if not rows:
                search_results.config(text="No Results!!")
            else:
                search_results.config(text=f"{len(rows)} reservation(s) found")

                for rid,name,flight_number,seat_number,departure,destination,date in rows: 
                    reservations_list.insert(tkinter.END,
                                             f"{rid} | name: {name} | flight no. {flight_number} | seat no. {seat_number} | departure: {departure} | destination: {destination} | date: {date} ")

        except Exception as e: 
            messagebox.showerror("ERROR", f"Cant show reservations .\n {e}")


    def selected_for_edit():
        selected = reservations_list.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reservation to edit/delete!")
            return 
        
        selected_text = reservations_list.get(selected[0])
        rid = int(selected_text.split("|")[0].strip())
        name = selected_text.split("name:")[1].split("|")[0].strip()
        flight_number = selected_text.split("flight no.")[1].split("|")[0].strip()
        seat_number = selected_text.split("seat no.")[1].split("|")[0].strip()
        departure = selected_text.split("departure: ")[1].split("|")[0].strip()
        destination = selected_text.split("destination: ")[1].split("|")[0].strip()
        date = selected_text.split("date: ")[1].strip()
        
        update_delete_page(reservations_window, rid, name, flight_number, seat_number, departure, destination, date, load_data)

    update_delete_button = tkinter.Button(reservations_window, text="Update/Delete", command=selected_for_edit, font=("Ariel",14,"bold"), fg="White", bg="Red")
    update_delete_button.pack(pady=5, anchor="center")


    refresh_button = tkinter.Button(reservations_window, text= "Refresh Button", command=load_data, font=("Ariel",14,"bold"),fg="White",bg="Red")    
    refresh_button.pack(pady= 10, anchor="center") 
    

    load_data()   




           

     

      
    

 

