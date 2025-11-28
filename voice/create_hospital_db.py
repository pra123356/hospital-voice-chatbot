import sqlite3
import os

# Full path to your project folder
project_folder = r"C:\Users\praga\Desktop\voice"
db_path = os.path.join(project_folder, "hospital.db")

# Connect to DB (creates file if not exists)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create table only if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    floor TEXT NOT NULL,
    department TEXT NOT NULL,
    admitted_on TEXT
)
''')

# Insert sample data ONLY if table is empty
cur.execute("SELECT COUNT(*) FROM patients")
if cur.fetchone()[0] == 0:
    sample_data = [
        ('Ramesh', '204', '2nd', 'Cardiology', '2025-10-01'),
        ('Priya', '101', '1st', 'Neurology', '2025-10-05'),
        ('Suresh', '303', '3rd', 'Orthopedic', '2025-10-09'),
        ('Anita', '405', '4th', 'Pediatrics', '2025-10-02'),
        ('Rajesh', '108', '1st', 'ENT', '2025-10-11')
    ]
    cur.executemany('''
    INSERT INTO patients (name, room_no, floor, department, admitted_on)
    VALUES (?, ?, ?, ?, ?)
    ''', sample_data)
    print("✅ Sample data inserted into 'patients' table.")

conn.commit()
conn.close()

print(f"✅ Database 'hospital.db' is ready at:\n{db_path}")
