import sqlite3
import pandas as pd
import streamlit as st


@st.cache_data
def get_data(query, db="patient_management.db"):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.sidebar.title("Patient Management Dashboard")
menu = st.sidebar.radio(
    "Select an Option:", ["Patients", "Appointments", "Medical History"]
)

if menu == "Patients":
    st.title("👩‍⚕️ Patients Overview")

    query = "SELECT * FROM Patients"
    patients = get_data(query)
    st.write("### Patient Records")
    st.dataframe(patients)

    st.write("### Statistics")
    st.write(f"Total Patients: {len(patients)}")
    st.bar_chart(patients["age"].value_counts())

elif menu == "Appointments":
    st.title("📅 Appointments Overview")
    query = """
    SELECT Appointments.*, Patients.name AS patient_name
    FROM Appointments
    JOIN Patients ON Appointments.patient_id = Patients.id
    """
    appointments = get_data(query)
    st.write("### Appointment Records")
    st.dataframe(appointments)

    st.write("### Statistics")
    st.write(f"Total Appointments: {len(appointments)}")
    st.bar_chart(appointments["doctor"].value_counts())

elif menu == "Medical History":
    st.title("📋 Medical History Overview")
    query = """
    SELECT MedicalHistory.*, Patients.name AS patient_name
    FROM MedicalHistory
    JOIN Patients ON MedicalHistory.patient_id = Patients.id
    """
    history = get_data(query)
    st.write("### Medical History Records")
    st.dataframe(history)

    st.write("### Most Common Conditions")
    st.bar_chart(history["condition"].value_counts())

st.sidebar.info("Developed with ❤️ using Streamlit")
