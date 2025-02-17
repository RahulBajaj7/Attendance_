import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import dropbox
import os

# Dropbox Access Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFhE9YEYauFF2QfQ9K5SOcWthDBHKAcZ-OsCHjwOlm6jsmNimQGKXnpe1tLG6FoOZuVOv5nHXJ--Z3hZ1h04KeE1clYbyzGNg5Mh4A0j6fJPHFET810_LJxoNdy_AVtdb4sGlbnBOlwMLeFlwaITeC6_bU8LSzWgcKq1tH7u0TfNAOnNITsAufWhzAS4llN_rYFyP4qv3p5kwojBOdkZV_Ekd7bN9Ovg6p5wmvgn8CzA4VxyE7n1CzbMshol3XzRuFwegSsVgagcJTyOJnWEm2ks4o92_IW5W3RQ-zm9Y0CXyZctUI3Bdpfwpftmdt8yDUboUumv22UOETjrVYtYHUZ7WA-paFL_iBib4R2thFCoRqca7qZ8YP6ORrgN4O3jPyEAMkdl8ybSzacZ-eM6l4v704Xmk6rToThoZIrJx13xQlbR7-08S8fkyID4CS7IScwYq_0O2zTdjezeoQYdtBRDMEDC7Aar6Wo7Hx9RJjgAFKb1oSciAFmyViy7cngbrqWybvv7L9pHrm8pZ5G4Vtq47PnkrVzFDnt9xFo2EnPxb_sEyLSRgK1Xh3FzaW_T3XceEzUAeCZgs2VPasSt3VC0QiIVkftkIBant89bJaDeCyAGWTrb2fBCSNBO7KshRDhinb02zL4Xt2mtb8mNwUjeYPt9d2u2_iaF6o5ss5eNgy8-Qkas_hT_pLiGZI4iq2z62wzhW-fKfsv1dASPLQLjhjvBpHkFvQ4fuVBx-4GJrG-zHk8Kn0mh6tjy7C7CueCi0pH6D8Q3kzPP4LG3UovOgDPVVdVJPFvDKPisHBl4I6Z2IDRXKlPMEcpjDL6Dg8sfxK7ta5tf0zZUbwQL7v6eOOGHVq5KCMWSVXkuHlHcdRYAIDmQ78OdEgiZOBXEwtL_I4MewbA0_oaYeC5-YKLw9JZHhSBPMnml5n-3GCN5e2Ig_XlqenRDYEbdxX0onyzyhWqxHsIYCGTN_gi-lgkkJbtoznUdBgA7u3C4eaIvlG7Nx6CD3jZNCHgZSLmWlzbR46FBYc-NhYf2_1brBmklAPAckmcuCR6SzgVIv7v2_IMpGwFyY9sRy036jPYoM_InmfyuiXDY6fSduVTV3WN_7h6RZHjTkfHh_YqZkBWo7ZlTBR3KcoGI6QZczhtDRm232KDAuclRMPsV58Y3vMbqSy8625O18zpDQSZCnIPP6pdRqATf1EvJXA5XNzLBB2g5DBwKMw2WY369yELPxpF3l7cLizE47FfsxqP_d5qpA6fDLhAJljhvkPRbP9Q84QnGviMZqtlq4CRIFjxpICnXKswflkruJICqfXGvCbSsNSc0ynn_qr3QrQ7mnHvrHmbMmMccO5wB6SdLAZH_Hz_yu_2J69BmYsdPLJKjBwRq3VketUmiNUpp1xqlMtyNU0bJQ2umA_BTcLP-i1-ABLaffzK2jXOBe-e8UJUIy6O37Ae"

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

