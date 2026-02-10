import sqlite3
import os

def migrate_database():
    # Check if database exists
    if not os.path.exists('hospital.db'):
        print("Database does not exist. Run the application first to create it.")
        return
    
    # Connect to the database
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    # Check if the new columns exist
    cursor.execute("PRAGMA table_info(billing)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    print("Current billing table columns:")
    for column in columns:
        print(f"  {column[1]} ({column[2]})")
    
    # If the new columns don't exist, we need to migrate
    if 'room_charges_per_day' not in column_names:
        print("\nMigrating database schema...")
        
        # Check if there's existing data
        cursor.execute("SELECT COUNT(*) FROM billing")
        count = cursor.fetchone()[0]
        print(f"Found {count} existing billing records")
        
        billing_data = []  # Initialize the variable
        
        if count > 0:
            # Backup existing data
            print("Backing up existing data...")
            cursor.execute("SELECT * FROM billing")
            billing_data = cursor.fetchall()
            
            # Create backup table
            cursor.execute('''
                CREATE TABLE billing_backup AS 
                SELECT * FROM billing
            ''')
            print("Backup created")
        
        # Drop the old table
        cursor.execute("DROP TABLE billing")
        
        # Create the new table with updated schema
        cursor.execute('''
            CREATE TABLE billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                consultation_fee REAL DEFAULT 0,
                medicine_charges REAL DEFAULT 0,
                room_charges_per_day REAL DEFAULT 0,
                number_of_days INTEGER DEFAULT 1,
                other_charges REAL DEFAULT 0,
                total_amount REAL DEFAULT 0,
                billing_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        # If we had data, restore it
        if count > 0 and billing_data:
            print("Restoring data with new schema...")
            for record in billing_data:
                # Extract values from old record
                # Old schema: id, patient_id, consultation_fee, medicine_charges, room_charges, other_charges, total_amount, billing_date
                old_id, patient_id, consultation_fee, medicine_charges, room_charges, other_charges, total_amount, billing_date = record
                
                # Insert into new table (assuming room_charges was for 1 day)
                cursor.execute('''
                    INSERT INTO billing (
                        id, patient_id, consultation_fee, medicine_charges, 
                        room_charges_per_day, number_of_days, other_charges, total_amount, billing_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (old_id, patient_id, consultation_fee, medicine_charges, room_charges, 1, other_charges, total_amount, billing_date))
        
        # Commit changes
        conn.commit()
        print("Database migration completed successfully!")
    else:
        print("\nDatabase is already up to date.")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    migrate_database()