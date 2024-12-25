import sqlite3
from faker import Faker
import random

fake = Faker()


def generate_patients(n=50):
    patients = []
    for _ in range(n):
        name = fake.name()
        first_name = name.split()[0]
        last_name = name.split()[-1]
        email = f"{first_name[0].lower()}{last_name.lower()}@example.com"
        age = random.randint(18, 90)
        gender = random.choice(["Male", "Female", "Other"])
        phone = fake.phone_number()
        patients.append((name, age, gender, email, phone))
    return patients


def generate_appointments(patient_ids, n=100, include_future=False):
    appointments = []
    for _ in range(n):
        patient_id = random.choice(patient_ids)
        appointment_date = fake.date_between(start_date="today", end_date="+10d")

        doctor = fake.name()
        appointments.append((patient_id, appointment_date, doctor))
    return appointments


def generate_medical_history(patient_ids, n=100):
    conditions = [
        "Healthy",
        "Minor Illness",
        "Chronic Condition",
        "Critical Condition",
        "Under Observation",
    ]
    medical_history = []
    for _ in range(n):
        patient_id = random.choice(patient_ids)
        condition = random.choice(conditions)
        diagnosis_date = fake.date_between(start_date="-5y", end_date="today")
        medical_history.append((patient_id, condition, diagnosis_date))
    return medical_history


def populate_database():
    conn = sqlite3.connect("patient_management.db")
    cursor = conn.cursor()
    patients = generate_patients()
    cursor.executemany(
        "INSERT INTO Patients (name, age, gender, email, phone) VALUES (?, ?, ?, ?, ?)",
        patients,
    )
    conn.commit()

    cursor.execute("SELECT id FROM Patients")
    patient_ids = [row[0] for row in cursor.fetchall()]

    appointments = generate_appointments(patient_ids)
    cursor.executemany(
        "INSERT INTO Appointments (patient_id, appointment_date, doctor) VALUES (?, ?, ?)",
        appointments,
    )
    conn.commit()

    medical_history = generate_medical_history(patient_ids)
    cursor.executemany(
        "INSERT INTO MedicalHistory (patient_id, condition, diagnosis_date) VALUES (?, ?, ?)",
        medical_history,
    )
    conn.commit()

    conn.close()
    print("Database populated with fake data!")


if __name__ == "__main__":
    populate_database()
