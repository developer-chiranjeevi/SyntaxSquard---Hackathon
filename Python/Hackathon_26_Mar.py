import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("medical_records.db")
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Create a table with patient details and diagnostic data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            patient_name TEXT NOT NULL,
            date TEXT NOT NULL,
            diagnostics TEXT NOT NULL  -- Stores 500-600 words
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database and table created successfully!")

def insert_patient_data(patient_id, patient_name, date, diagnostics):
    # Connect to SQLite database
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    
    # Insert patient data
    try:
        cursor.execute("INSERT INTO patients (patient_id, patient_name, date, diagnostics) VALUES (?, ?, ?, ?)", 
                       (patient_id, patient_name, date, diagnostics))
        conn.commit()
        print(f"Patient data inserted successfully for Patient ID: {patient_id}")
    except sqlite3.IntegrityError:
        print(f"Error: Patient ID {patient_id} already exists.")
    
    conn.close()

def get_patient_data(patient_id):
    # Connect to SQLite database
    conn = sqlite3.connect("medical_records.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    cursor = conn.cursor()
    
    # Fetch patient data by ID
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    # Convert row to dictionary
    if row:
        return dict(row)
    return None

if __name__ == "__main__":
    create_database()
    
    # Example: Insert a new patient record
    insert_patient_data(1, "Perumal", "26-03-25", "Patient shows signs of mild fever, cough, and fatigue.")
    insert_patient_data(2, "Sakthi", "27-03-25", "Patient has a history of diabetes and high blood pressure.")
    insert_patient_data(3, "Sangu", "28-03-25", "Patient has a dengue fever.")
    insert_patient_data(4, "Srikanth", "29-03-25", "Patient has a symptoms of heart attack.")
    
    # Example: Read data for a specific patient ID
    patient_id = int(input("Enter Patient ID to retrieve data: "))
    data = get_patient_data(patient_id)
    
    if data:
        print("Patient Data:", data)
    else:
        print("No record found for the given Patient ID.")
