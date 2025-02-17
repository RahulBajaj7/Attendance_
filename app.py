import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import dropbox
import os

# Dropbox Access Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFjvhlGamTvI12OrZYIu7mdgtoHz_BqFpJGJRU7_WIV2NVSURvLofyhEWFsEck72RMEi2TLA6ffoSMcvTkRTweZhhAYm9X_9U9W9KRlgbvWS45Akqut0YF6V55qylpWiRN8xh-gRJVP92D-Ns77t4HT2d9RKGYjjGtpg23kTQpgXkQab6d7pphyK3U391eLd0qxDy3xi-0D9v9Px3tFaiqncJPOKmNAgl3iB_upEdY5bATMRwWU6zRLVOH7pNtN2P1QTt3Gm0F_97TdTC8PeuoQgRsJqVs9hI_5ULyCz-L4mYBberY8wJdshQplmk1bdx24l11tx0fSQlx59q9Uc18RxXzBblCBDWw3A7bQJwValKsQGWghec6qvQd3er9KFtMU46SkePikvuiHgWdB8JWg3ex-TR9oZu4CyBkBHZI_vGYnRqELbaqZ1L9eIhqNBYP7yowhUJUZENVHfBTlclUaiRPuFWy5rYCH6Zh7r0haqLVAngQ1kjGT5Kwn9NS4fq_sMQ2d4QfzZ5OoYRzdRrAfBN32hWoUx2y20I9VfyKH4U361W8L7jSruoui8nAVq58X2dwg-xXKNfYsLOXkUL7NATT_9Wu95TFoHt8ueTHPUS1fY_DAtxR8HxcKlbTgiXWl1ZpjafkDCFJBffgKtbCOann9S2mWdP7UmNsMyyicZKrmxdoiwno1cc_-HNJvcDP3XSXek7xGWiXEQGfmM5BiCp9fKu-QPk6ELMPJ3Y-vr26jXBrffOCRLfzlITIExW3NvmIagvmXK4xaPHhtquAMIJFVFfytNIczZyjjuZ6IOS4robF4qgpO_kY23PXK-li2GWut6vTGGgRjM0ALOMFkfOsSL5SEGokG6aE2Za0iRBauUNvi4f5IW-ACklgBUwKCZS9tWWIZpqA8TRZCskFP8TJOJKgMI97FFJgvzIuVQXXQcKJu1fUWwOoUuKzl-HofUbJdlZaam2goMYQda2rs0VlN8glcQdj3oMQv8tSdB8V6WAuHKfz49bq36WF72p5Jn5IbOnQffHz8_BV8ZjNqqsFsc5fTQEfqxdsyyfdLolpKkA12gFs_mjajVnfgIg70PG110LFTuMCqNmoJ-RNPzu8ClNZ0Y4RLKCtQ1y3WZYkKHzSCbyW5N_3C03n0QCCZ1LwmGrSP9M5Ys4U_fIhAjINs4Oib8URKLq6P7crBpmBprNMjH0I2_s4ql-MCHgYD2WZIH1aCCmH3wqtU2k-Kf35An6X7LiT6QyrM23kDz4-OJQKVRfy-UROQobxX8h4O9A4-VOe6CT5BPFyR0WEY-bmB_zbLNQnBGmGIpVRfM0_kIg_yaiOhKneK1JYQaGu1cv8fESD-w5XkV_go9ymv8WVf8iclWaCcf0W5ywJMSVYDXSVKnNXSXvO8DK9kHBUPa8Cczun_sLVpf9pzJ7DuOwQg4845O_aIrKANKH6mhUw"

# Set up Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

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
    "BIPBI": 20  # New subject added
}

# File path for saving attendance data
ATTENDANCE_FILE = "attendance_data.csv"

# Load attendance data
def load_attendance():
    if "attendance" not in st.session_state:
        if os.path.exists(ATTENDANCE_FILE):
            df = pd.read_csv(ATTENDANCE_FILE)
            attendance_dict = df.to_dict(orient="list")

            # Ensure all subjects exist in attendance state
            for subject in subjects:
                if subject not in attendance_dict:
                    attendance_dict[subject] = []

            st.session_state.attendance = attendance_dict
        else:
            st.session_state.attendance = {subject: [] for subject in subjects}

# Save attendance data to Dropbox
def save_attendance_to_dropbox():
    max_length = max(len(lst) for lst in st.session_state.attendance.values())
    for subject in subjects:
        while len(st.session_state.attendance[subject]) < max_length:
            st.session_state.attendance[subject].append(False)
    df = pd.DataFrame.from_dict(st.session_state.attendance)

    # Save locally first
    df.to_csv(ATTENDANCE_FILE, index=False)

    # Upload to Dropbox
    try:
        with open(ATTENDANCE_FILE, "rb") as f:
            dbx.files_upload(f.read(), f'/attendance/{ATTENDANCE_FILE}', mute=True)
        st.success("Attendance data uploaded to Dropbox successfully!")
    except Exception as e:
        st.error(f"Error uploading to Dropbox: {e}")

# Load data on startup
load_attendance()

# Title and Visualization
st.title("📊 Attendance Dashboard")

# Donut Chart Visualization
st.subheader("📊 Attendance Visualization")
cols = st.columns(3)
for idx, (subject, max_classes) in enumerate(subjects.items()):
    attended_list = st.session_state.attendance.get(subject, [])
    conducted = len(attended_list)
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
    save_attendance_to_dropbox()

