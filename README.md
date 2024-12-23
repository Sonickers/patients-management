# 🏥 Patient Management Dashboard

This project is a simple **Patient Management System** built using SQLite for the database and Python for generating fake data and visualizing data through a dashboard.

---

## ✨ Features
- 🗂️ **Database**: 
  - SQLite database with three tables:
    - **`Patients`**: Stores patient details.
    - **`Appointments`**: Tracks appointments with doctors.
    - **`MedicalHistory`**: Logs patients' medical history.
- 🛠️ **Data Population**:
  - Python script to populate the database with fake data using the `Faker` library.
- 📊 **Future Extension**:
  - Interactive Python-based dashboard for visualization and data interaction.

---

## 🗄️ Database Schema
### Patients Table
| Column  | Type     | Description               |
|---------|----------|---------------------------|
| `id`    | Integer  | Primary Key (Auto Increment) |
| `name`  | Text     | Patient's Name            |
| `age`   | Integer  | Patient's Age             |
| `gender`| Text     | Gender                    |
| `email` | Text     | Email Address             |
| `phone` | Text     | Phone Number              |

### Appointments Table
| Column              | Type     | Description                     |
|---------------------|----------|---------------------------------|
| `id`                | Integer  | Primary Key (Auto Increment)   |
| `patient_id`        | Integer  | Foreign Key referencing `Patients.id` |
| `appointment_date`  | Date     | Date of Appointment            |
| `doctor`            | Text     | Doctor's Name                  |

### MedicalHistory Table
| Column            | Type     | Description                     |
|-------------------|----------|---------------------------------|
| `id`              | Integer  | Primary Key (Auto Increment)   |
| `patient_id`      | Integer  | Foreign Key referencing `Patients.id` |
| `condition`       | Text     | Medical Condition              |
| `diagnosis_date`  | Date     | Date of Diagnosis              |
