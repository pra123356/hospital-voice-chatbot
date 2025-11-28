import sqlite3

# -------------------------
# Connect to database
# -------------------------
# Using absolute path to avoid OneDrive issues
db_path = r"C:\Users\praga\Desktop\voice\hospital.db"
conn = sqlite3.connect(db_path, timeout=10)
cursor = conn.cursor()

# -------------------------
# Drop tables if they exist
# -------------------------
cursor.execute("DROP TABLE IF EXISTS availability")
cursor.execute("DROP TABLE IF EXISTS doctors")

# -------------------------
# Create doctors table
# -------------------------
cursor.execute('''
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    specialization TEXT
)
''')

# -------------------------
# Create availability table
# -------------------------
cursor.execute('''
CREATE TABLE availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    day DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status TEXT DEFAULT 'Available',
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
''')

# -------------------------
# Insert doctors
# -------------------------
doctors = [
    ("Dr. Mehta", "mehta@example.com", "123"),
    ("Dr. Sancheti", "sancheti@example.com", "123"),
    ("Dr. Anjali Sharma", "anjali@example.com", "123"),
    ("Dr. Rajesh Mehta", "rajesh@example.com", "123"),
    ("Dr. Priya Nair", "priya@example.com", "123"),
    ("Dr. Arjun Kapoor", "arjun@example.com", "123"),
    ("Dr. Kavita Rao", "kavita@example.com", "123"),
    ("Dr. Amit Joshi", "amit@example.com", "123")
]

cursor.executemany(
    "INSERT OR IGNORE INTO doctors (name, email, password) VALUES (?,?,?)",
    doctors
)

# -------------------------
# Insert sample availability
# -------------------------
availability = [
    # Doctor 1
    (1, "2025-10-12", "10:00", "11:00"),
    (1, "2025-10-12", "11:00", "12:00"),
    # Doctor 2
    (2, "2025-10-13", "09:00", "10:00"),
    (2, "2025-10-13", "10:00", "11:00"),
    # Doctor 3
    (3, "2025-10-14", "14:00", "15:00"),
    (3, "2025-10-14", "15:00", "16:00"),
    # Doctor 4
    (4, "2025-10-15", "09:00", "10:00"),
    (4, "2025-10-15", "10:00", "11:00"),
]

cursor.executemany(
    "INSERT OR IGNORE INTO availability (doctor_id, day, start_time, end_time) VALUES (?,?,?,?)",
    availability
)

# -------------------------
# Commit changes
# -------------------------
conn.commit()

# -------------------------
# Verify inserted doctors
# -------------------------
cursor.execute("SELECT * FROM doctors")
doctors_rows = cursor.fetchall()
print(f"Doctors in table: {len(doctors_rows)}")
for row in doctors_rows:
    print(row)

# -------------------------
# Verify availability
# -------------------------
cursor.execute("SELECT * FROM availability")
availability_rows = cursor.fetchall()
print(f"\n Availability slots in table: {len(availability_rows)}")
for row in availability_rows:
    print(row)

# -------------------------
# Close connection
# -------------------------
conn.close()
print("\n Database initialized successfully!")
