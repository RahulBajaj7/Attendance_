import streamlit as st
import pandas as pd
import dropbox
from dropbox.files import WriteMode
import io

# Subject details
subjects = {
    "LAB": 10,
    "RL": 10,
    "BDMA": 20,
    "DLM": 20,
    "OSCM": 20,
    "C&S": 20,
    "BIPBI": 20  # New subject added
}

# Dropbox API Setup
DROPBOX_ACCESS_TOKEN = "YOUR_DROPBOX_ACCESS_TOKEN"  # Replace with your access token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Load attendance data
def load_attendance():
    if "attendance" not in st.session_state:
        st.session_state.attendance = {subject: [] for subject in subjects}

# Save attendance data to Dropbox
def save_attendance():
    # Convert the attendance data to DataFrame
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in st.session_state.attendance.items()]))
    
    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False)
    
    # Save the CSV file to Dropbox
    try:
        file_path = "/attendance_data.csv"  # Path where you want to save the file in Dropbox
        file = io.BytesIO(csv_data.encode('utf-8'))  # Convert string to bytes
        dbx.files_upload(file.read(), file_path, mode=WriteMode("overwrite"))
        st.success("Attendance data saved to Dropbox successfully!")
    except Exception as e:
        st.error(f"Error saving data to Dropbox: {str(e)}")

# Load data on startup
load_attendance()

# Title and Visualization
st.title("📊 Attendance Dashboard")

# Sidebar Attendance Summary
st.sidebar.header("🎯 Goal Tracking (80% Target)")
summary = []
for subject, max_classes in subjects.items():
    attended_list = st.session_state.attendance.get(subject, [])
    conducted = len(attended_list)
    attended = sum(attended_list)
    percentage = (attended / conducted * 100) if conducted > 0 else 0
    summary.append({"Subject": subject, "Conducted": conducted, "Attended": attended, "Percentage": percentage})
    
    if percentage < 80:
        st.sidebar.warning(f"{subject}: {percentage:.2f}% (Below Goal)")
    else:
        st.sidebar.success(f"{subject}: {percentage:.2f}% (On Track)")

# Attendance Input Section
st.subheader("📌 Mark Attendance")
for subject, max_classes in subjects.items():
    st.write(f"### {subject} (Max: {max_classes})")
    conducted = len(st.session_state.attendance.get(subject, []))
    conducted = st.number_input(f"Sessions Conducted for {subject}", 
                                min_value=0, max_value=max_classes, 
                                value=conducted, step=1, key=f"{subject}_conducted")
    
    st.session_state.attendance[subject] = st.session_state.attendance[subject][:conducted]
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)
    
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Session {i+1}", 
                                                              value=st.session_state.attendance[subject][i], 
                                                              key=f"{subject}_session_{i+1}")

# Display summary table
summary_df = pd.DataFrame(summary)
st.subheader("📄 Attendance Summary")
st.dataframe(summary_df)

# Save attendance data when button is clicked
if st.button("💾 Save Attendance to Dropbox"):
    save_attendance()

