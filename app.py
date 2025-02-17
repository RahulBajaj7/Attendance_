import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import dropbox
from dropbox.exceptions import AuthError

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

# Dropbox details
DROPBOX_ACCESS_TOKEN = "sl.u.AFjO2rkjk8b3ZS7p_jazZayclOZD1uvKbIqXwtltxtxFsRRnjuUMrATmc_BLIdkig-dS426PIUveLngFpY2IXGN3k_9VJKU4--oD8oeobtVHj6UGmaxCU_qFoDY1w_-S-IRlthR57lY887nK2i-yHVi2K89RQn5rD2oxgbt0hYgpp7PhxTJtBRdp5CXN97j1XnAjzTW4qlkbqK-lNmKd62qRfJO3OIv22_ENBZNpJgDV0rUn8DmRgw4iQ3LRkL7iVKvxAFrx_0jQ1Bx-xGkbY07cUZxpJNqLq_kEQ2MxApR442mCkefywJ30yjrEOKctfr3x0bVT3KioUSAhIp-wdB2O6hoBbj2vKgQM1JR1o8-9_SDiXhHLz7m___NrSoQqnN-IoblMfL6GJLDZhgKdj2opGNWBVtjusjEDiqkc-aqKquGoB34Yo1p5Jk7CfeI0EnH7i0MFxPxiN8QOXbLCQtX5KDJHNHIYXN9uTl-9HmS-vo9ijXWasEp3lG5D5rEZY2ZNsxbkhuAszj0BTuZYh72ez385AkUTOyVhAYuqwLDUrzdrPITKSA5QAH2hmkR5mbPgE-gSCWkgKr7zB5OlHPZVa9un1YDSXkSPlibLoNrZELmw_xH7pzvlUbL1bSE5uzlb87qhm3uao_tardbtPDigZNiTpmIv4Vm8xzbnUoFzvBgrYPvRfb-4M8OVFznzgFKsKuv-bND5OS-w1pMDzkes9kH-BkkOkIesZYdbcv_ubYcoQo19iN1gLRcdYQa4mLbxKIjk9L8-xLCXg1t4jAoDsaEV4ipX5xj4yCzMsHfnx0rGoW0rcOzrkWASHGhcF0KPZrksJLhi9BMkqG4t3vAK65s42tRnJh-kVRcilPlt1nLjNZND-0PioYMMyWg_hx2MBBkt1qN6OpOoDtGGgewDe_OsoptK5D5Ih8eDAcVEIrJQMc2DCqHZs0ohd3nsDJvrVU3Flp63wWKIuWvIqpAi0bq4Zr5hmsfAKNjxexJsF9jxxgY08bCWzpea2DluyFGwr023gWBmYNLX0T_CB5Zd9TQfPaztwD5q1dyTWoxjFUC_QG9jikxGnGg0gjmJAHPkE_im8cbUcVmHK_yNYKPJgekqd2tkHGZCC37vt66oO8x9vM7LJi7sBp_BRA1cWfa0D67--n6XZRzeeSrVEKUyWCMrkOyu8tSM27I-w2dvWqreCk5jgOJWxFbR3h9gTskI1alieZdItxw1__Ny1pKGVXjCWN4VwyuKRjHXftDbzhDkd0KF0IUzFPkDB75-Wk9Ibj4VDIzsX8VKBWzPFxOiykK7iNRBcnwA67WT7WIzv3YVgzxVA9-v9CDhp5CFba44OXfGF1u3p_LZOtQKi9wwPnGxq9k4sKsJDwIF_Iyp4Dqb3_r4vEoMwsNcU9XT4gLCG0JFELIWm9vcHR3j-niGOwwtJc54QxHdV0Ly4PhUrQ"
DROPBOX_FOLDER_PATH = "/attendance_data"
DROPBOX_FILE_NAME = "attendance_data.csv"

# Dropbox client setup
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# File path for saving attendance data
ATTENDANCE_FILE = "attendance_data.csv"

# Load attendance data
def load_attendance():
    if "attendance" not in st.session_state:
        try:
            # Try to download the file from Dropbox
            _, res = dbx.files_download(DROPBOX_FOLDER_PATH + "/" + DROPBOX_FILE_NAME)
            df = pd.read_csv(res.raw)
            attendance_dict = df.to_dict(orient="list")

            # Ensure all subjects exist in attendance state
            for subject in subjects:
                if subject not in attendance_dict:
                    attendance_dict[subject] = []

            st.session_state.attendance = attendance_dict
        except Exception as e:
            # If no file, initialize empty attendance data
            st.session_state.attendance = {subject: [] for subject in subjects}

# Save attendance data to Dropbox
def save_attendance():
    max_length = max(len(lst) for lst in st.session_state.attendance.values())
    for subject in subjects:
        while len(st.session_state.attendance[subject]) < max_length:
            st.session_state.attendance[subject].append(False)

    df = pd.DataFrame.from_dict(st.session_state.attendance)

    # Save the updated data to Dropbox
    try:
        # Upload to Dropbox, overwrite the existing file
        dbx.files_upload(df.to_csv(index=False).encode(), DROPBOX_FOLDER_PATH + "/" + DROPBOX_FILE_NAME, mode=dropbox.files.WriteMode("overwrite"))
        st.success("Attendance data saved successfully to Dropbox!")
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
    
    # Ensure that the input is within the allowed range
    conducted = st.number_input(f"Sessions Conducted for {subject}",
                                min_value=0, max_value=max_classes, 
                                value=len(st.session_state.attendance.get(subject, [])),
                                step=1, key=f"{subject}_conducted")
    
    # Truncate the list to the number of conducted sessions
    st.session_state.attendance[subject] = st.session_state.attendance[subject][:conducted]
    
    # Add checkboxes for each session conducted
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
if st.button("💾 Save Attendance"):
    save_attendance()
