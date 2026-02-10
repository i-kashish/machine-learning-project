import sqlite3

try:
    # Connect to the database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    # Check table structure
    cursor.execute("PRAGMA table_info(billing)")
    columns = cursor.fetchall()
    
    print("Billing table structure:")
    for column in columns:
        print(f"  {column[1]} ({column[2]})")
        
    # Check if any data exists
    cursor.execute("SELECT COUNT(*) FROM billing")
    count = cursor.fetchone()[0]
    print(f"\nNumber of records in billing table: {count}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")