import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("medical_records.db")
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
    
    conn.commit()
    conn.close()
    print("Database and table created successfully!")

def insert_patient_data():
    # Connect to SQLite database
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    
    while True:
        try:
            # Get user input
            patient_id = int(input("Enter Patient ID: "))
            patient_name = input("Enter Patient Name: ")
            date = input("Enter Date (DD-MM-YY): ")
            diagnostics = input("Enter Diagnostic Details: ")
            
            # Insert data into the database
            cursor.execute("INSERT INTO patients (patient_id, patient_name, date, diagnostics) VALUES (?, ?, ?, ?)", 
                           (patient_id, patient_name, date, diagnostics))
            conn.commit()
            print(f"Patient data inserted successfully for Patient ID: {patient_id}")
        
        except sqlite3.IntegrityError:
            print(f"Error: Patient ID {patient_id} already exists.")
        except ValueError:
            print("Invalid input! Please enter numerical values for Patient ID.")
        
        # Ask if user wants to add another record
        more = input("Do you want to add another record? (yes/no): ").strip().lower()
        if more != "yes":
            break
    
    conn.close()

def get_patient_data():
    # Connect to SQLite database
    conn = sqlite3.connect("medical_records.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    cursor = conn.cursor()
    
    try:
        patient_id = int(input("Enter Patient ID to retrieve data: "))
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        row = cursor.fetchone()
        
        if row:
            print("Patient Data:", dict(row))
        else:
            print("No record found for the given Patient ID.")
    
    except ValueError:
        print("Invalid input! Please enter a valid Patient ID.")
    
    conn.close()

if __name__ == "__main__":
    create_database()
    
    while True:
        print("\nMenu:")
        print("1. Insert Patient Data")
        print("2. Retrieve Patient Data")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            insert_patient_data()
        elif choice == "2":
            get_patient_data()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please enter a valid option.")
