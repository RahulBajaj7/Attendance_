import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Subject details
subjects = {
    "LAB": 10,
    "RL": 10,
    "BDMA": 20,
    "DLM": 20,
    "OSCM": 20,
    "C&S": 20,
}

# Initialize attendance data
if "attendance" not in st.session_state:
    st.session_state.attendance = {subject: [] for subject in subjects}

st.title("Attendance Dashboard")

# Attendance Input Section
st.subheader("Mark Attendance")
for subject, max_classes in subjects.items():
    st.write(f"### {subject} (Max Classes: {max_classes})")
    
    # Input for classes conducted so far
    conducted = st.number_input(f"Classes Conducted for {subject}", min_value=0, max_value=max_classes, value=len(st.session_state.attendance[subject]), step=1, key=f"{subject}_conducted")
    
    # Ensure attendance list matches the number of conducted classes
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)
    while len(st.session_state.attendance[subject]) > conducted:
        st.session_state.attendance[subject].pop()
    
    # Checkboxes for marking attendance
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Class {i+1}", value=st.session_state.attendance[subject][i], key=f"{subject}_class_{i+1}")

# Attendance Summary and Visualizations
st.subheader("Attendance Summary")

summary = []
for subject, max_classes in subjects.items():
    conducted = len(st.session_state.attendance[subject])
    attended = sum(st.session_state.attendance[subject])
    percentage = (attended / conducted * 100) if conducted > 0 else 0
    summary.append({"Subject": subject, "Conducted": conducted, "Attended": attended, "Percentage": percentage})

# Display summary in a table
summary_df = pd.DataFrame(summary)
st.dataframe(summary_df)

# Donut Chart Visualization
st.subheader("Attendance Visualization")
for subject in subjects.keys():
    conducted = len(st.session_state.attendance[subject])
    attended = sum(st.session_state.attendance[subject])
    missed = conducted - attended
    percentage = (attended / conducted * 100) if conducted > 0 else 0
    
    # Donut chart
    fig = go.Figure(data=[go.Pie(
        labels=["Attended", "Missed"],
        values=[attended, missed],
        hole=0.5,
        textinfo="label+percent"
    )])
    fig.update_layout(
        title=f"{subject}: {percentage:.2f}% Attendance",
        annotations=[dict(text=f"{percentage:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
    )
    st.plotly_chart(fig)

# Attendance Goal Check
st.subheader("Goal Tracking (80% Target)")
for subject in subjects.keys():
    percentage = summary_df[summary_df["Subject"] == subject]["Percentage"].values[0]
    if percentage < 80:
        st.warning(f"{subject} is below the 80% attendance goal! Current: {percentage:.2f}%")
    else:
        st.success(f"{subject} is meeting the attendance goal! Current: {percentage:.2f}%")
