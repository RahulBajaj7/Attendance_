import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from io import StringIO

# Set page config
st.set_page_config(layout="wide")

# Subject details
subjects = {
    "LAB": 10,
    "RL": 10,
    "BDMA": 20,
    "DLM": 20,
    "OSCM": 20,
    "C&S": 20,
}

# GitHub raw URL for the CSV file
GITHUB_RAW_URL = "https://raw.githubusercontent.com/RahulBajaj7/Attendance_/main/Data.csv"

# Load attendance data from GitHub
def load_attendance():
    if "attendance" not in st.session_state:
        try:
            # Fetch the raw CSV data from GitHub
            response = requests.get(GITHUB_RAW_URL)
            response.raise_for_status()  # Check if request was successful
            csv_data = response.text
            df = pd.read_csv(StringIO(csv_data))
            st.session_state.attendance = df.set_index('Subject').T.to_dict(orient="list")
        except Exception as e:
            st.session_state.attendance = {subject: [] for subject in subjects}
            st.error(f"Error loading data from GitHub: {e}")

# Save attendance data (locally for this session)
def save_attendance():
    df = pd.DataFrame.from_dict(st.session_state.attendance, orient="index").transpose()
    df.to_csv("attendance_data.csv", index=False)

# Load data on startup
load_attendance()

# Title and Visualization
st.title("📊 Attendance Dashboard")

# Donut Chart Visualization
st.subheader("📊 Attendance Visualization")
cols = st.columns(3)
for idx, (subject, max_classes) in enumerate(subjects.items()):
    conducted = len(st.session_state.attendance.get(subject, []))
    attended = sum(st.session_state.attendance.get(subject, []))
    missed = conducted - attended
    percentage = (attended / conducted * 100) if conducted > 0 else 0

    fig = go.Figure(data=[go.Pie(
        labels=["Attended", "Missed"],
        values=[attended, missed],
        hole=0.5,
        textinfo="label+percent"
    )])
    fig.update_layout(
        title=f"{subject}: {percentage:.2f}% Attendance",
        annotations=[dict(text=f"{percentage:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    cols[idx % 3].plotly_chart(fig, use_container_width=True)

# Sidebar Attendance Summary
st.sidebar.header("🎯 Goal Tracking (80% Target)")
summary = []
for subject, max_classes in subjects.items():
    conducted = len(st.session_state.attendance.get(subject, []))
    attended = sum(st.session_state.attendance.get(subject, []))
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
    conducted = st.number_input(f"Sessions Conducted for {subject}", min_value=0, max_value=max_classes, 
                                value=len(st.session_state.attendance.get(subject, [])), step=1, key=f"{subject}_conducted")
    
    # Ensure list length matches conducted classes
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)
    while len(st.session_state.attendance[subject]) > conducted:
        st.session_state.attendance[subject].pop()
    
    # Checkbox for each session
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Session {i+1}", 
                                                              value=st.session_state.attendance[subject][i], 
                                                              key=f"{subject}_session_{i+1}")

# Display summary table
summary_df = pd.DataFrame(summary)
st.subheader("📄 Attendance Summary")
st.dataframe(summary_df)

# Save attendance data when button is clicked
if st.button("💾 Save Attendance"):
    save_attendance()
    st.success("Attendance data saved successfully!")


