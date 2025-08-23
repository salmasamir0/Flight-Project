import sqlite3

def remove_duplicate_reservations():
    """Remove duplicate reservations from the database, keeping only one copy of each unique combination with sequential IDs"""
    
    try:
        conn = sqlite3.connect("flights.db")
        cursor = conn.cursor()
        
        # Get unique reservations (without IDs)
        cursor.execute("""
            SELECT name, flight_number, seat_number
            FROM reservations
            GROUP BY name, flight_number, seat_number
            ORDER BY MIN(id)
        """)
        unique_reservations = cursor.fetchall()
        
        # Delete all reservations
        cursor.execute("DELETE FROM reservations")
        
        # Reset the auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='reservations'")
        
        # Insert back unique reservations with sequential IDs (starting from 1)
        for name, flight_number, seat_number in unique_reservations:
            cursor.execute("""
                INSERT INTO reservations (name, flight_number, seat_number) 
                VALUES (?, ?, ?)
            """, (name, flight_number, seat_number))
        
        unique_count = len(unique_reservations)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database cleanup completed!")
        print(f"📊 Kept {unique_count} unique reservations")
        print(f"🔢 IDs are now sequential (1, 2, 3, ...)")
        print("🗑️ All duplicates have been removed")
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")

if __name__ == "__main__":
    print("🧹 Starting database cleanup...")
    remove_duplicate_reservations()
