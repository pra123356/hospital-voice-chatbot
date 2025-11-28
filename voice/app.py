from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import date as dt

app = Flask(__name__)
app.secret_key = "supersecret"

# ======================================================
# 🧩 DATABASE CONNECTION
# ======================================================
def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

# ======================================================
# 🏠 HOMEPAGE + GENERAL ROUTES
# ======================================================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/payment.html")
def payment():
    return render_template("payment.html")

@app.route("/navigation")
def navigation():
    return render_template("navigation.html")

@app.route("/queue")
def queue():
    return render_template("queue.html")

@app.route("/check_existing")
def check_existing():
    return render_template("check_existing.html")

@app.route("/appointment_booking")
def appointment_booking():
    selected_doctor_id = request.args.get("doctor_id", "")
    return render_template("appointment_booking.html", selected_doctor_id=selected_doctor_id)



# ======================================================
# 👨‍⚕️ DOCTOR MODULE
# ======================================================
@app.route("/doctor/login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if doctor:
            session["doctor_id"] = doctor["doctor_id"]
            session["doctor_name"] = doctor["name"]
            flash("Login successful!", "success")
            return redirect(url_for("doctor_dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("doctor_login.html")


@app.route("/doctor/dashboard")
def doctor_dashboard():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    slots = conn.execute(
        "SELECT * FROM availability WHERE doctor_id=? ORDER BY day, start_time",
        (session["doctor_id"],)
    ).fetchall()
    conn.close()

    return render_template("doctor_dashboard.html",
                           doctor=session["doctor_name"],
                           slots=slots)


@app.route("/doctor/set_availability")
def set_availability():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))
    return render_template("set_availability.html")


@app.route("/doctor/add_availability", methods=["POST"])
def add_availability():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    day = request.form["day"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    status = request.form["status"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO availability (doctor_id, day, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)",
        (session["doctor_id"], day, start_time, end_time, status)
    )
    conn.commit()
    conn.close()

    flash("Availability slot added successfully!", "success")
    return redirect(url_for("doctor_dashboard"))


@app.route("/doctor/view_availability")
def doctor_view_availability():
    if "doctor_id" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    availability = conn.execute(
        "SELECT id, day, start_time, end_time, status FROM availability WHERE doctor_id=? ORDER BY day, start_time",
        (session["doctor_id"],)
    ).fetchall()
    conn.close()

    return render_template("doctor_view_availability.html", availability=availability)


@app.route("/doctor/delete_availability/<int:slot_id>", methods=["POST"])
def delete_availability(slot_id):
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM availability WHERE id=? AND doctor_id=?",
                 (slot_id, session["doctor_id"]))
    conn.commit()
    conn.close()

    flash("Availability slot deleted successfully!", "info")
    return redirect(url_for("doctor_view_availability"))


@app.route("/doctor/logout")
def doctor_logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("doctor_login"))


# ======================================================
# 📅 DOCTOR AVAILABILITY (PUBLIC VIEW)
# ======================================================
@app.route("/availability", methods=["GET", "POST"])
def view_availability():
    conn = get_db_connection()
    if request.method == "POST":
        selected_day = request.form.get("date")
    else:
        selected_day = dt.today().strftime("%Y-%m-%d")

    doctors = conn.execute("""
        SELECT d.name, d.specialization, a.start_time, a.end_time
        FROM doctors d
        JOIN availability a ON d.doctor_id = a.doctor_id
        WHERE a.day = ?
    """, (selected_day,)).fetchall()
    conn.close()

    return render_template("availability.html", doctors=doctors, date=selected_day)


# ======================================================
# 🧾 PATIENT REGISTRATION (used by form submission)
# ======================================================
@app.route("/submit.html", methods=["POST"])
def patient_register():
    name = request.form["name"]
    phone = request.form["phone"]
    aadhar = request.form["aadhar"]
    email = request.form["email"]
    gender = request.form["gender"]
    age = request.form["age"]
    address = request.form["address"]

    # ⏰ Get Current IST Date & Time
    from datetime import datetime
    import pytz

    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)
    created_date = now.strftime("%Y-%m-%d")
    created_time = now.strftime("%H:%M:%S")

    conn = get_db_connection()

    # ✅ Create table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            aadhar TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER,
            address TEXT NOT NULL
        )
    """)

    # ✅ Add created_date and created_time columns if they don't exist
    columns = [row["name"] for row in conn.execute("PRAGMA table_info(patients1)").fetchall()]
    if "created_date" not in columns:
        conn.execute("ALTER TABLE patients1 ADD COLUMN created_date TEXT")
    if "created_time" not in columns:
        conn.execute("ALTER TABLE patients1 ADD COLUMN created_time TEXT")

    # Insert patient with date & time
    conn.execute("""
        INSERT INTO patients1
        (name, phone, aadhar, email, gender, age, address, created_date, created_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, aadhar, email, gender, age, address, created_date, created_time))

    conn.commit()
    conn.close()

    flash("Patient registered successfully!", "success")
    return redirect(url_for("payment"))


# ======================================================
# 🧍‍♀️ PATIENT APPOINTMENT (Aadhaar-based retrieval)
# ======================================================
@app.route("/appointment", methods=["POST"])
def check_existing_patient():
    aadhar = request.form.get("aadhar")

    conn = get_db_connection()
    patient = conn.execute("SELECT * FROM patients1 WHERE aadhar=?", (aadhar,)).fetchone()
    conn.close()

    if patient:
        flash(f"Welcome back, {patient['name']}! Your details are preloaded.", "info")
        return render_template(
            "appointment_booking1.html",
            name=patient["name"],
            phone=patient["phone"],
            aadhar=patient["aadhar"],
            email=patient["email"],
            gender=patient["gender"],
            age=patient["age"],
            address=patient["address"]
        )
    else:
        flash("New patient detected. Please fill your details to continue.", "warning")
        return redirect(url_for("appointment_booking"))


# ✅ AJAX route for real-time patient retrieval
@app.route("/get_patient", methods=["POST"])
def get_patient():
    data = request.get_json()
    aadhar = data.get("aadhar")

    conn = get_db_connection()
    patient = conn.execute(
        "SELECT name, gender, phone, address, email, age FROM patients1 WHERE aadhar=?",
        (aadhar,)
    ).fetchone()
    conn.close()

    if patient:
        return jsonify({
            "status": "found",
            "name": patient["name"],
            "gender": patient["gender"],
            "phone": patient["phone"],
            "address": patient["address"],
            "email": patient["email"],
            "age": patient["age"]  # <-- add this line
        })
    else:
        return jsonify({"status": "not_found"})
    
    # ======================================================
# 🆕 APPOINTMENT SUBMISSION → Save into patients2
# ======================================================
@app.route("/appointment_submit", methods=["POST"])
def appointment_submit():
    name = request.form["name"]
    phone = request.form["phone"]
    aadhar = request.form["aadhar"]
    email = request.form["email"]
    gender = request.form["gender"]
    age = request.form["age"]
    address = request.form["address"]

    # Get IST date & time
    from datetime import datetime
    import pytz
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)
    created_date = now.strftime("%Y-%m-%d")
    created_time = now.strftime("%H:%M:%S")

    conn = get_db_connection()

    # Create table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            aadhar TEXT NOT NULL,
            email TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER,
            address TEXT NOT NULL,
            created_date TEXT,
            created_time TEXT
        )
    """)

    # Insert (duplicates allowed)
    conn.execute("""
        INSERT INTO patients2
        (name, phone, aadhar, email, gender, age, address, created_date, created_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, aadhar, email, gender, age, address, created_date, created_time))

    conn.commit()
    conn.close()

    flash("Appointment details saved!", "success")

    return redirect(url_for("payment"))

# ======================================================
# Navigation
# ======================================================
@app.route("/get_patient_room", methods=["POST"])
def get_patient_room():
    data = request.get_json()
    name = data.get("name", "").strip().lower()
    
    # Remove any quotes or punctuation
    import re
    name = re.sub(r"[^a-zA-Z]", "", name)  # keeps only letters
    
    print("Cleaned spoken name:", repr(name))

    conn = get_db_connection()
    patient = conn.execute("""
        SELECT name, room_no, floor, department
        FROM patients
        WHERE REPLACE(LOWER(TRIM(name)), ' ', '') LIKE ?
        LIMIT 1
    """, (f"%{name}%",)).fetchone()
    conn.close()

    if patient:
        text = f"{patient['name']} is in room {patient['room_no']}, on the {patient['floor']} floor, in the {patient['department']} department."
        return jsonify({"response": text})

    return jsonify({"response": "Patient not found."})

# ======================================================
# 📅 SELECT AVAILABLE DOCTORS PAGE (NEW ROUTE)
# ======================================================
from datetime import datetime, date as dt
import pytz

@app.route("/select_doctor")
def select_doctor():
    conn = get_db_connection()

    # Current IST date & time
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)
    current_day = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # Fetch only doctors available at this time
    doctors = conn.execute("""
        SELECT d.doctor_id, d.name, d.specialization, d.image_path
        FROM doctors d
        JOIN availability a ON d.doctor_id = a.doctor_id
        WHERE a.day = ?
          AND a.start_time <= ?
          AND a.end_time >= ?
          AND a.status = 'Available'
        GROUP BY d.doctor_id
    """, (current_day, current_time, current_time)).fetchall()
    conn.close()

    return render_template("select_doctor.html", doctors=doctors)

# ======================================================
#  RUN APP
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)




# ======================================================
#  RUN APP
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)