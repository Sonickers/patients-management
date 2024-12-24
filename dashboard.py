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
    "Select an Option:", ["Patients", "Appointments", "Medical History", "Analytics"]
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

st.sidebar.info("Developed with ❤️ using Streamlit")

if menu == "Analytics":
    st.title("📊 Advanced Analytics")

    query_appointments = "SELECT * FROM Appointments"
    query_medical_history = "SELECT * FROM MedicalHistory"

    appointments = get_data(query_appointments)
    medical_history = get_data(query_medical_history)

    appointments["appointment_date"] = pd.to_datetime(appointments["appointment_date"])

    st.subheader("Busy Days Analysis")
    appointments["day_of_week"] = appointments["appointment_date"].dt.day_name()
    busy_days = appointments["day_of_week"].value_counts()
    st.bar_chart(busy_days)

    st.subheader("Trends in Appointments Over Time")
    appointments["date"] = appointments["appointment_date"].dt.date
    appointments_trend = appointments.groupby("date").size()
    st.line_chart(appointments_trend)

    st.subheader("Common Conditions")
    condition_counts = medical_history["condition"].value_counts()
    st.bar_chart(condition_counts)

    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        st.subheader("Condition Word Cloud")
        condition_text = " ".join(medical_history["condition"].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            condition_text
        )

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    except ImportError:
        st.info("Install the `wordcloud` package to enable the word cloud feature.")


elif menu == "Analytics":
    st.title("📊 Advanced Analytics")

    query_appointments = "SELECT * FROM Appointments"
    query_medical_history = "SELECT * FROM MedicalHistory"

    appointments = get_data(query_appointments)
    medical_history = get_data(query_medical_history)

    appointments["appointment_date"] = pd.to_datetime(appointments["appointment_date"])

    st.subheader("Busy Days Analysis")
    appointments["day_of_week"] = appointments["appointment_date"].dt.day_name()
    busy_days = appointments["day_of_week"].value_counts()
    st.bar_chart(busy_days)

    st.subheader("Trends in Appointments Over Time")
    appointments["date"] = appointments["appointment_date"].dt.date
    appointments_trend = appointments.groupby("date").size()
    st.line_chart(appointments_trend)

    st.subheader("Common Conditions")
    condition_counts = medical_history["condition"].value_counts()
    st.bar_chart(condition_counts)

    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        st.subheader("Condition Word Cloud")
        condition_text = " ".join(medical_history["condition"].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            condition_text
        )

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    except ImportError:
        st.info("Install the `wordcloud` package to enable the word cloud feature.")
