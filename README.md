#  AI Voice-Based Hospital Receptionist System 
An advanced voice-enabled hospital receptionist system that automates patient registration, appointment booking, doctor availability management, queue handling, payment, and navigation assistance through an intelligent voice interface.

##  Overview 
This project is a **complete hospital front-desk automation system** using **Virtual Receptionist System**.  Patients talk to the system, and it performs tasks like:
- Registration through voice  
- Appointment booking  
- Checking doctor availability  
- Token & queue management  
- Navigation inside hospital  
- Retrieving existing patient info  
- Doctor login & availability setup 

All data is stored in SQLite (hospital.db).

##  Voice-Based Features 
The AI receptionist supports:
- Asking questions verbally  
- Auto-filling forms  
- Guiding throughout the process  
- Providing spoken confirmations 

#  System Modules 

### **1️. Doctor Login & Availability Management**  
Doctors log in using **email and password** from the database:

Example doctor records:  
1 Dr. Mehta mehta@example.com
 Cardiology
2 Dr. Sancheti sancheti@example.com
 ENT

 Doctors can set:
- Start time  
- End time  
- Date  
- Availability (Available / Not Available)

Stored as:
id doctor_id start_time end_time status
1 1 10:00 11:00 Available
2 1 11:00 12:00 Available
3 2 09:00 10:00 Available
4 2 10:00 11:00 Available

Patients can view this under **"Doctor Availability"**.

### **2️. Appointment Booking**  

System asks:  
**“Are you an existing patient?”**

###  If NO (New Patient)  
- It fetches only doctors who are **available at the current time**  
- Displays full doctor profile (image, specialization, email)  
- Patient selects doctor  
- System opens Registration Form  

###  Registration Form Fields:  
- Full Name  
- Phone  
- Aadhar  
- Email  
- Gender  
- Age  
- Address  
- Created Date  
- Created Time  
- Selected doctor_id  

Saved in SQLite table `patients1`.

###  After Submit
- Payment options displayed  
- Token generated  
- Confirmation shown to patient  

### **3️. Existing Patient Lookup**  
If patient says:  
 “Yes, I am an existing patient”

The system retrieves their previous records from SQLite:
- Name  
- Phone  
- Aadhar  
- Email  
- Age  
- Gender  
- Address  

Data is **pre-filled automatically**.  
Then after confirm:
- Doctor selection  
- Payment  
- Token generation  

### **4️. Queue & Token Management**  
In **Queue Section**, patient can check:
- Their token number  
- Total waiting patients  
- Estimated waiting time  

Data fetched live from SQLite.

### ** 5️. Navigation Assistance**  
Relatives can say patient name to find:
- Room number  
- Floor  
- Department 

# Technologies Used  

### **Frontend**
- HTML  
- CSS  
- JavaScript  

### **Backend**
- Python Flask  
- SpeechRecognition  
- SQLite (`hospital.db`)  

### **Database**
- SQLite · Doctor table  
- Availability table  
- Patients table  
- Navigation table  

#  Project Folder Structure  
project/
│
├── app.py
├── hospital.db
├── create_hospital_db.py
├── init_db.py
│
├── static/
│ ├── images/
│ └── styles.css
│
└── templates/
├── index.html
├── appointment_booking.html
├── appointment_booking1.html
├── availability.html
├── chatbot.html
├── check_existing.html
├── doctor_dashboard.html
├── doctor_login.html
├── doctor_view_availability.html
├── navigation.html
├── payment.html
├── queue.html
├── select_doctor.html
└── set_availability.html

# How to Run the Project 
### 1️. Install Requirements
pip install flask speechrecognition pyttsx3 pandas

### 2️. Run the Backend 
python app.py

#  Workflow Summary  
1. Patient speaks → System understands  
2. If new patient → Registration  
3. If existing → Details fetched  
4. Shows available doctors  
5. Patient selects doctor  
6. Payment options shown  
7. Token generated & stored  
8. Queue + Navigation options available

# Future Improvements  
- Multi-language support (Hindi/Marathi)  
- OTP verification  
- Automated calling system  
- WhatsApp appointment system  
- Integration with hospital MIS  
- Voice-based navigation map  
