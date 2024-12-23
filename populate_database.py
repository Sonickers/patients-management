import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = sqlite3.connect("patient_management.db")
cursor = conn.cursor()


def generate_patients(n=50):
    patients = []
    for _ in range(n):
        name = fake.name()
        age = random.randint(1, 90)
        gender = random.choice(["Male", "Female", "Other"])
        email = fake.email()
        phone = fake.phone_number()
        patients.append((name, age, gender, email, phone))
    return patients


def generate_appointments(patient_ids, n=100):
    appointments = []
    for _ in range(n):
        patient_id = random.choice(patient_ids)
        appointment_date = fake.date_between(start_date="-2y", end_date="today")
        doctor = fake.name()
        reason = fake.sentence(nb_words=6)
        appointments.append((patient_id, appointment_date, doctor, reason))
    return appointments


def generate_medical_history(patient_ids, n=100):
    medical_history = []
    for _ in range(n):
        patient_id = random.choice(patient_ids)
        condition = fake.word()
        diagnosis_date = fake.date_between(start_date="-5y", end_date="today")
        treatment = fake.sentence(nb_words=10)
        medical_history.append((patient_id, condition, diagnosis_date, treatment))
    return medical_history


def populate_database():
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
        "INSERT INTO Appointments (patient_id, appointment_date, doctor, reason) VALUES (?, ?, ?, ?)",
        appointments,
    )
    conn.commit()

    medical_history = generate_medical_history(patient_ids)
    cursor.executemany(
        "INSERT INTO MedicalHistory (patient_id, condition, diagnosis_date, treatment) VALUES (?, ?, ?, ?)",
        medical_history,
    )
    conn.commit()


if __name__ == "__main__":
    populate_database()
    print("Database populated with fake data!")
    conn.close()
