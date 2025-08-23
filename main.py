import tkinter
from tkinter import messagebox
import sqlite3
import dataBase
from reservations import open_reservations_page
from edit_reservations import update_delete_page

def main_window():
    window = tkinter.Tk()
    window.title("Flight Reservation App.")
    window.geometry("600x400")

    label = tkinter.Label(window, text="Welcome to Flight Reservation App", font=("Times New Roman",22,"bold"), fg ="darkblue")
    label.pack(pady= 50 , anchor="center")

    def open_bookingpage():
      booking_window = tkinter.Toplevel(window)
      booking_window.title("Booking Page")
      booking_window.geometry("500x600") 

      label_booking = tkinter.Label(booking_window, text="Welcome to the Booking Page",font=("Times New Roman",20,"bold"), fg="Black")
      label_booking.pack(pady= 5, anchor= "center")

      label_name = tkinter.Label(booking_window, text="Name: ", font=("Ariel",18,"italic"), fg="blue")
      label_name.pack(pady= 5, anchor= "w")
      entry_name = tkinter.Entry(booking_window)
      entry_name.pack(pady= 5 , anchor= "w")

      label_flight = tkinter.Label(booking_window, text="Flight Number: ",font=("Ariel",18,"italic"), fg="blue" )
      label_flight.pack(pady= 10 , anchor="w")
      entry_flight = tkinter.Entry(booking_window)
      entry_flight.pack(pady= 5 , anchor= "w")

      label_seat = tkinter.Label(booking_window, text= "Seat Number: ", font=("Ariel",18,"italic"), fg="blue")
      label_seat.pack(pady= 10, anchor="w")
      entry_seat = tkinter.Entry(booking_window)
      entry_seat.pack(pady= 5, anchor= "w")

      label_departure = tkinter.Label(booking_window, text= "Departure: ", font=("Ariel",18,"italic"), fg="blue")
      label_departure.pack(pady = 10 , anchor= "w")
      entry_departure = tkinter.Entry(booking_window)
      entry_departure.pack(pady= 5, anchor="w")

      label_destination = tkinter.Label(booking_window, text="Destination: ", font=("Ariel",18,"italic"), fg="blue")
      label_destination.pack(pady=10, anchor= "w")
      entry_destination = tkinter.Entry(booking_window)
      entry_destination.pack(pady= 5, anchor= "w")

      label_date = tkinter.Label(booking_window, text="Flight Date: ", font=("Ariel",18,"italic"), fg="blue")
      label_date.pack(pady= 10, anchor= "w")
      entry_date = tkinter.Entry(booking_window)
      entry_date.pack(pady= 5, anchor="w")


      def confirm_booking():
          name = entry_name.get().strip()
          flight_number = entry_flight.get().strip()
          seat_number = entry_seat.get().strip()
          departure = entry_departure.get().strip()
          destination = entry_destination.get().strip()
          date = entry_date.get().strip()

          # Validate input fields
          if not name or not flight_number or not seat_number or not departure or not destination or not date:
              tkinter.messagebox.showerror("Error", "Please fill in all fields!")
              return

          try:
              with sqlite3.connect("flights.db") as conn:
                  cursor = conn.cursor()
                  
                  # Check if this exact reservation already exists
                  cursor.execute("SELECT COUNT(*) FROM reservations WHERE name=? AND flight_number=? AND seat_number=? AND departure =? AND destination =? AND date =?", 
                                (name, flight_number, seat_number, departure, destination, date))
                  if cursor.fetchone()[0] > 0:
                      tkinter.messagebox.showwarning("Duplicate Booking", "This reservation already exists!")
                      return
                  
                  # Insert new reservation
                  cursor.execute("INSERT INTO reservations (name, flight_number, seat_number, departure, destination, date) VALUES (?, ?, ?, ?, ?, ?)", 
                                (name, flight_number, seat_number, departure, destination, date))
                  conn.commit()
                  
                  # Clear input fields after successful booking
                  entry_name.delete(0, tkinter.END)
                  entry_flight.delete(0, tkinter.END)
                  entry_seat.delete(0, tkinter.END)
                  entry_departure.delete(0, tkinter.END)
                  entry_destination.delete(0, tkinter.END)
                  entry_date.delete(0, tkinter.END)
                  
                  tkinter.messagebox.showinfo("Success", "Booking confirmed successfully!")
                  print("Booking Confirmed!!")
                  
          except Exception as e:
              tkinter.messagebox.showerror("Database Error", f"Failed to save booking: {e}")

      button_confirm = tkinter.Button(booking_window, text="Confirm Booking", font=("Ariel",14,"bold"),fg="Red", command=confirm_booking)
      button_confirm.pack(pady= 10, anchor="center")  


    button_booking = tkinter.Button(window, text= "Book Flight", command=open_bookingpage, font=("Arial",14),fg="black", bg="white" )
    button_booking.pack(anchor="center")

    button_reservations = tkinter.Button(window, text="View Reservations", command=lambda: open_reservations_page(window), font=("Ariel",14), fg="black", bg="white" )
    button_reservations.pack(anchor="center", pady= 50) 

   
    window.mainloop()  

main_window()     

if __name__ == "__main__":
    main_window()





