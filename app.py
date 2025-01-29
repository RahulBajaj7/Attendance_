import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

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

# File path for saving attendance data
ATTENDANCE_FILE = "attendance_data.csv"

# Load attendance data
def load_attendance():
    if "attendance" not in st.session_state or "conducted_sessions" not in st.session_state:
        if os.path.exists(ATTENDANCE_FILE):
            df = pd.read_csv(ATTENDANCE_FILE)
            
            # Initialize session state if missing
            if "attendance" not in st.session_state:
                st.session_state.attendance = {}
            if "conducted_sessions" not in st.session_state:
                st.session_state.conducted_sessions = {}

            # Restore attendance records
            for subject in subjects:
                if subject in df.columns:
                    st.session_state.attendance[subject] = df[subject].dropna().astype(bool).tolist()
                else:
                    st.session_state.attendance[subject] = []

            # Restore conducted session count
            if "Conducted" in df.columns:
                conducted_dict = dict(zip(df["Subject"], df["Conducted"]))
                for subject in subjects:
                    st.session_state.conducted_sessions[subject] = conducted_dict.get(subject, 0)
            else:
                for subject in subjects:
                    st.session_state.conducted_sessions[subject] = 0
        else:
            # Initialize empty data
            st.session_state.attendance = {subject: [] for subject in subjects}
            st.session_state.conducted_sessions = {subject: 0 for subject in subjects}

# Save attendance data
def save_attendance():
    # Ensure conducted session count is included
    attendance_data = {
        "Subject": [],
        "Conducted": [],
    }

    for subject in subjects:
        conducted = st.session_state.conducted_sessions.get(subject, 0)
        attendance_data["Subject"].append(subject)
        attendance_data["Conducted"].append(conducted)

    # Save attendance status as columns
    for subject, attendance_list in st.session_state.attendance.items():
        max_length = max(len(lst) for lst in st.session_state.attendance.values())
        st.session_state.attendance[subject] = attendance_list[:conducted]  # Trim to conducted count
        while len(st.session_state.attendance[subject]) < max_length:
            st.session_state.attendance[subject].append(False)
        attendance_data[subject] = st.session_state.attendance[subject]

    # Convert dictionary to DataFrame
    df = pd.DataFrame(attendance_data)
    df.to_csv(ATTENDANCE_FILE, index=False)

# Load data on startup
load_attendance()

# Title and Visualization
st.title("📊 Attendance Dashboard")

# Donut Chart Visualization
st.subheader("📊 Attendance Visualization")
cols = st.columns(3)
for idx, (subject, max_classes) in enumerate(subjects.items()):
    attended_list = st.session_state.attendance.get(subject, [])
    conducted = st.session_state.conducted_sessions.get(subject, 0)
    attended = sum(attended_list)
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
    conducted = st.session_state.conducted_sessions.get(subject, 0)
    attended_list = st.session_state.attendance.get(subject, [])
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
    conducted = st.number_input(f"Sessions Conducted for {subject}", min_value=0, max_value=max_classes, 
                                value=st.session_state.conducted_sessions.get(subject, 0), step=1, key=f"{subject}_conducted")
    
    # Store conducted count in session state
    st.session_state.conducted_sessions[subject] = conducted

    # Adjust attendance list to match conducted count
    st.session_state.attendance[subject] = st.session_state.attendance[subject][:conducted]  # Trim excess
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)  # Fill missing sessions
    
    # Checkbox for each session
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Session {i+1}", 
                                                              value=st.session_state.attendance[subject][i], 
                                                              key=f"{subject}session{i+1}")

# Display summary table
summary_df = pd.DataFrame(summary)
st.subheader("📄 Attendance Summary")
st.dataframe(summary_df)

# Save attendance data when button is clicked
if st.button("💾 Save Attendance"):
    save_attendance()
    st.success("Attendance data saved successfully!")
