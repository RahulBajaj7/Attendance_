import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body {background-color: black; color: white;}
        .stDataFrame {color: white !important;}
    </style>
""", unsafe_allow_html=True)

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

st.title("📊 Attendance Dashboard")

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
    conducted = st.number_input(f"Classes Conducted for {subject}", min_value=0, max_value=max_classes, value=len(st.session_state.attendance[subject]), step=1, key=f"{subject}_conducted")
    
    while len(st.session_state.attendance[subject]) < conducted:
        st.session_state.attendance[subject].append(False)
    while len(st.session_state.attendance[subject]) > conducted:
        st.session_state.attendance[subject].pop()
    
    for i in range(conducted):
        st.session_state.attendance[subject][i] = st.checkbox(f"Class {i+1}", value=st.session_state.attendance[subject][i], key=f"{subject}_class_{i+1}")

# Display summary table
summary_df = pd.DataFrame(summary)
st.subheader("📄 Attendance Summary")
st.dataframe(summary_df.style.set_properties(**{'background-color': 'black', 'color': 'white'}))

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
        textinfo="label+percent",
        marker=dict(colors=["#32CD32", "#FF4500"])
    )])
    fig.update_layout(
        title=f"{subject}: {percentage:.2f}% Attendance",
        annotations=[dict(text=f"{percentage:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor="black",
        font=dict(color="white")
    )
    
    cols[idx % 3].plotly_chart(fig, use_container_width=True)

