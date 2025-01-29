import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# Load attendance data if it exists
if "attendance" not in st.session_state:
    try:
        df = pd.read_csv("attendance_data.csv")
        st.session_state.attendance = df.to_dict(orient="list")
    except FileNotFoundError:
        st.session_state.attendance = {subject: [] for subject in subjects}

# Function to save attendance data
def save_attendance():
    df = pd.DataFrame.from_dict(st.session_state.attendance, orient="index").transpose()
    df.to_csv("attendance_data.csv", index=False)

# Title and Visualization
st.title("📊 Attendance Dashboard")

# Donut Chart Visualization (3 in a row)
st.subheader("📊 Attendance Visualization")
cols = st.columns(3)
for idx, (subject, max_classes) in enumerate(subjects.items()):
    conducted = len(st.session_state.attendance[subject])
    attended = sum(st.session_state.attendance[subject])
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

# Attendance Summary (Top Right)
st.sidebar.header("🎯 Goal Tracking (80% Target)")
summary = []
for subject, max_classes in subjects.items():
    conducted = len(st.session_state.attendance[subject])
    attended = sum(st.session_state.attendance[subject])
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
    conducted = st.number_input(f"Sessions Conducted for {subject}", min_value=0, max_value=max_classes, value=len(st.session_state.attendance[subject]), step=1, key=f"{subject}_conducted")
    
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)
    while len(st.session_state.attendance[subject]) > conducted:
        st.session_state.attendance[subject].pop()
    
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Session {i+1}", value=st.session_state.attendance[subject][i], key=f"{subject}_session_{i+1}")

# Display summary table
summary_df = pd.DataFrame(summary)
st.subheader("📄 Attendance Summary")
st.dataframe(summary_df)

# Save attendance data
save_attendance()



