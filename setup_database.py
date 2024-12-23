import sqlite3


def setup_database():
    conn = sqlite3.connect("patient_management.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        appointment_date DATE NOT NULL,
        doctor TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients (id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS MedicalHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        condition TEXT NOT NULL,
        diagnosis_date DATE NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients (id)
    )
    """
    )

    conn.commit()
    conn.close()
    print("Database setup complete!")


if __name__ == "__main__":
    setup_database()
