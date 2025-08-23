import tkinter
import dataBase
import sqlite3
from tkinter import messagebox 

global update_delete_page 

def update_delete_page(reservations_window, rid, name, flight_number, seat_number, departure, destination, date, load_data):
    update_delete_window = tkinter.Toplevel(reservations_window)
    update_delete_window.title("Update/Delete Window")
    update_delete_window.geometry("400x350")

    update_label = tkinter.Label(update_delete_window, text="Update Reservations Here", font=("Times New Roman",20,"bold"), fg="Red")
    update_label.pack(pady= 5, anchor="center")

    label_name = tkinter.Label(update_delete_window, text="Name: ", font=("Ariel",18,"italic"), fg="Blue")
    label_name.pack(pady= 5, anchor="w")
    entry_name = tkinter.Entry(update_delete_window)
    entry_name.pack(pady= 5, anchor="e")
    entry_name.insert(0,name)

    label_flight = tkinter.Label(update_delete_window, text="Flight: ", font=("Ariel",18,"italic"), fg="Blue")
    label_flight.pack(pady= 10, anchor="w")
    entry_flight = tkinter.Entry(update_delete_window)
    entry_flight.pack(pady= 5, anchor="e")
    entry_flight.insert(0,flight_number)

    label_seat = tkinter.Label(update_delete_window, text="Seat: ", font=("Ariel",18,"italic"), fg="Blue")
    label_seat.pack(pady= 10, anchor="w")
    entry_seat = tkinter.Entry(update_delete_window)
    entry_seat.pack(pady= 5, anchor="e")
    entry_seat.insert(0,seat_number)

    label_departure = tkinter.label(update_delete_window, text="departure: ", font=("Ariel",18,"italic"), fg="Blue")
    label_departure.pack(pady= 10, anchor="w")
    entry_departure = tkinter.Entry(update_delete_window)
    entry_departure.pack(pady= 5, anchor="e")
    entry_departure.insert(0,departure)

    label_destination = tkinter.Label(update_delete_window, text="Final destination", font=("Ariel",18,"italic"), fg="Blue")
    label_destination.pack(pady= 5, anchor="w")
    entry_destination = tkinter.Entry(update_delete_window)
    entry_destination.pack(pady= 5 , anchor= "e")
    entry_destination.insert(0,destination)

    label_date = tkinter.Label(update_delete_window, text="Date: ", font=("Ariel",18,"italic"), fg="Blue")
    label_date.pack(pady= 10, anchor="w")
    entry_date = tkinter.Entry(update_delete_window)
    entry_date.pack(pady= 5 , anchor="e")
    entry_date.insert(0,date)

    def update_reservations():
        new_name = entry_name.get().strip()
        new_flight = entry_flight.get().strip()
        new_seat = entry_seat.get().strip()
        new_departure = entry_departure.get().strip()
        new_destination = entry_destination.get().strip()
        new_date = entry_date.get().strip()

        if not new_name or not new_flight or not new_seat or not new_departure or not new_destination or not new_date :
            messagebox.showerror("ERROR" , "Please enter your data")
            return 
        
        try:
            with sqlite3.connect("flights.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """ UPDATE reservations SET name = ? , flight_number = ? , seat_number = ?, departure = ?, destination = ?, date = ? WHERE id = ? """,
                     (new_name, new_flight, new_seat, new_departure, new_destination, new_date, rid)
                )
                conn.commit()

            messagebox.showinfo("Success" ,"Date Updated Successfully!")
            load_data()
            update_delete_window.destroy()

        except Exception as e:
            messagebox.showerror("Failed", f"Couldn't update data in database: {e}")

    def delete_reservatios():
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation ?")
        if not confirm: 
            return 
        
        try:
            with sqlite3.connect("flights.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""DELETE FROM reservations WHERE id=?""" , (rid,))

                if cursor.rowcount == 0:
                    messagebox.showwarning("Not Found","No reservation is deleted , maybe it was already deleted.")
                    return
                conn.commit()

                messagebox.showinfo("Success","Data successfully deleted")
                load_data()
                update_delete_window.destroy()

        except Exception as e:
            messagebox.showerror("Failed!", f"Database error: {e}")

    # Create and pack the buttons
    update_button = tkinter.Button(update_delete_window, text="Update", command=update_reservations, font=("Arial", 14, "bold"), fg="White", bg="Green")
    update_button.pack(pady=10, anchor="center")
    
    delete_button = tkinter.Button(update_delete_window, text="Delete", command=delete_reservatios, font=("Arial", 14, "bold"), fg="White", bg="Red")
    delete_button.pack(pady=5, anchor="center")
