import sqlite3

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

if count > 0:
    print("\nSample records:")
    cursor.execute("SELECT * FROM billing LIMIT 3")
    records = cursor.fetchall()
    for record in records:
        print(record)

conn.close()