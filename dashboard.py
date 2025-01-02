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
    "Select an Option:",
    [
        "Appointments View",
        "Patients",
        "Appointments",
        "Medical History",
        "Analytics",
        "Search",
    ],
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

elif menu == "Appointments View":
    st.title("📅 Appointments Calendar View")

    query = """
    SELECT Appointments.id, Appointments.appointment_date, Appointments.doctor, 
           Patients.name AS patient_name, Patients.age, Patients.gender, 
           MedicalHistory.condition, MedicalHistory.treatment
    FROM Appointments
    JOIN Patients ON Appointments.patient_id = Patients.id
    JOIN MedicalHistory ON Appointments.patient_id = MedicalHistory.patient_id
    GROUP BY Appointments.id
    """
    appointments = get_data(query)

    appointments["appointment_date"] = pd.to_datetime(
        appointments["appointment_date"], errors="coerce"
    )

    today = pd.Timestamp.now().normalize()
    future_window = today + pd.Timedelta(days=30)
    future_appointments = appointments[
        (appointments["appointment_date"] >= today)
        & (appointments["appointment_date"] <= future_window)
    ]

    st.write("### Upcoming Appointments (Today + 30 Days)")
    selected_appointment = st.selectbox(
        "Select an Appointment to View Details:",
        future_appointments["id"],
        format_func=lambda x: f"Appointment ID: {x}",
    )

    if selected_appointment:
        details = future_appointments[
            future_appointments["id"] == selected_appointment
        ].iloc[0]
        st.write(f"### Appointment Details")
        st.write(f"**Patient Name:** {details['patient_name']}")
        st.write(f"**Age:** {details['age']}")
        st.write(f"**Gender:** {details['gender']}")
        st.write(f"**Condition:** {details['condition']}")
        st.write(f"**Treatment:** {details['treatment']}")
        st.write(f"**Doctor:** {details['doctor']}")
        st.write(f"**Date:** {details['appointment_date'].strftime('%A, %d-%m-%Y')}")


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

    last_10_days = appointments[
        pd.to_datetime(appointments["appointment_date"])
        >= pd.Timestamp.now() - pd.Timedelta(days=10)
    ]
    if last_10_days.empty:
        st.write("No appointments in the last 10 days.")
    else:
        st.bar_chart(last_10_days["appointment_date"].value_counts())

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

elif menu == "Analytics":
    st.title("📊 Advanced Analytics")

    # Fetch appointment and medical history data
    query_appointments = """
    SELECT appointment_date, doctor, patient_id 
    FROM Appointments
    """
    query_medical_history = """
    SELECT condition, patient_id 
    FROM MedicalHistory
    """
    query_patients = """
    SELECT id, age, gender 
    FROM Patients
    """

    appointments = get_data(query_appointments)
    medical_history = get_data(query_medical_history)
    patients = get_data(query_patients)

    # Convert appointment_date to datetime
    appointments["appointment_date"] = pd.to_datetime(
        appointments["appointment_date"], errors="coerce"
    )

    # --- 1. Most Active Doctors ---
    st.subheader("Top Doctors by Number of Appointments")
    doctor_counts = appointments["doctor"].value_counts()
    st.bar_chart(doctor_counts)

    # --- 2. Most Common Conditions ---
    st.subheader("Most Common Conditions")
    condition_counts = medical_history["condition"].value_counts()
    st.bar_chart(condition_counts)

    # --- 3. Trends by Age and Gender ---
    st.subheader("Patient Demographics Analysis")
    # Merge patient demographics with medical history
    medical_history = medical_history.merge(
        patients, left_on="patient_id", right_on="id", how="inner"
    )

    st.write("### Condition Distribution by Age")
    medical_history["age_group"] = pd.cut(
        medical_history["age"],
        bins=[0, 18, 35, 50, 65, 100],
        labels=["0-18", "19-35", "36-50", "51-65", "65+"],
    )
    age_condition_counts = (
        medical_history.groupby(["age_group", "condition"]).size().unstack(fill_value=0)
    )
    st.bar_chart(age_condition_counts)

    st.write("### Gender Distribution by Condition")
    gender_condition_counts = (
        medical_history.groupby(["gender", "condition"]).size().unstack(fill_value=0)
    )
    st.bar_chart(gender_condition_counts)


elif menu == "Search":
    st.title("🔍 Search Appointments")

    query = """
    SELECT Appointments.id, Appointments.appointment_date, Appointments.doctor, 
           Patients.name AS patient_name
    FROM Appointments
    JOIN Patients ON Appointments.patient_id = Patients.id
    """
    appointments = get_data(query)

    search_term = st.text_input("Search by Patient or Doctor Name:")

    if search_term:
        filtered_appointments = appointments[
            (
                appointments["patient_name"].str.contains(
                    search_term, case=False, na=False
                )
            )
            | (appointments["doctor"].str.contains(search_term, case=False, na=False))
        ]

        if not filtered_appointments.empty:
            st.write("### Search Results:")
            st.dataframe(filtered_appointments)
        else:
            st.write("No matching records found.")


elif menu == "Analytics":
    st.title("📊 Advanced Analytics")

    query_appointments = "SELECT * FROM Appointments"
    query_medical_history = "SELECT * FROM MedicalHistory"

    appointments = get_data(query_appointments)
    medical_history = get_data(query_medical_history)

    appointments["appointment_date"] = pd.to_datetime(
        appointments["appointment_date"], errors="coerce"
    )

    st.subheader("Appointments Over Time")
    appointments["week"] = (
        appointments["appointment_date"].dt.to_period("W").astype(str)
    )
    appointments_trend = appointments.groupby("week").size()
    st.line_chart(appointments_trend)

    st.subheader("Most Common Medical Conditions")
    condition_counts = medical_history["condition"].value_counts()
    st.bar_chart(condition_counts)

    st.subheader("Top Doctors by Number of Appointments")
    top_doctors = appointments["doctor"].value_counts()
    st.bar_chart(top_doctors)

    st.subheader("Appointment Distribution Heatmap")
    appointments["day_of_week"] = appointments["appointment_date"].dt.day_name()
    appointments["hour"] = appointments["appointment_date"].dt.hour
    heatmap_data = appointments.pivot_table(
        index="day_of_week", columns="hour", aggfunc="size", fill_value=0
    )

    st.write("Heatmap: Appointments by Day and Hour")
    st.dataframe(heatmap_data)
