import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import dropbox
import os

# Dropbox Access Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFix1p8Ha04bX3rOGa8cnWRLoKYGKBTuH0jJvM1QbRYGt4AHoGeeefqsth_jOym6iekQNUpdKA1h7ShTNq7_SAmA6WbLU4udgJummA4TMA6NEuQxg688Z9fvQOOHj2kEfn9rIcRwNe_CcDi_oUhGzv7AvGAkeckh7VzOeVxD2k1CTLd38xNgtDJmMxzlldlxcDzthdi5wJ8BqiJ5GREDn8r_deqtGuizFrMM2RN80SmriJW_rg7lF_0PKoEzgzbH4UqePX7jpw2MUssF25ANbvttAM-2n2q0YrT2QoNjN77BIjRGFgBNGrCcaiG3kwY2WT5Kn1KpmDZfj4hp4bDQWKQik_9T_WkZZ6l-qnl-Y5Xla1BTr1ONgVNVhY84MdfdQ1rDhG7cmgXHFyCuy7hI_zi5wQSZLWB5wKmSnQmlGSjifTMtJJT9ii9Bq0hDGhCyTl7VYiaQA1_hkOj79FWAYg-ijydiMBLf7AkKishW3UUcUv4i6l96A0-wXgz5i3AR9vJH2Pz_Abi63s96BNei9Cei9B3w5Y7G4UT-rrkFUh6uTJAzJMpZL90kvo93jIwHvUWCyUGE8t7wNfOAVIqU5-I9J3gGtbVO23XeY8FhQxQ5-6yCu2MFTjdze1G7B9_noD2yv4rdIdZtSz0qxBhIDwT-sgfRzmMzXPb6mkxnECjvihlUzgtwcuUpG567sdEHTBzyuzZR2r59QU7DDNpNf4p5Iku4zpjYZdu4zAvlsEucSYRFmaqEjBoSLDfN6SuSqoJECcrFhnZdEvNHdBRzolo4CiT4PGBuQbCb8-HgEyTMnC7dTRpjeraucHrf_IKrJVs947qnzLFl0JIKeEbh9X7wJjJg5VJ5paBeXSYRc01bPBTgUpcAgFXV68nPJMjeAzFyc6Devque0NPVtyzWxMTFGzaxs08GJ9l5D9CsoTvBGjaXB9iXEHpczhDlWtJlhwl5rGZ3fA5XBSU9lwCfVvhcu3IsVOYuguugBmnIfGCyTpUqM-RoQAs2ZEJbD1uhNZ2eOBG_bi_G3PgwH6XWcvyYroEE0l_4t1NKlo-SM4W7XM99J6brikeMP33Pi0ZlDShLMChx1pzgWpSkSTYerRFkFO3fd2OppacxjlHxxrpoBaPAL9RPL2Qbq_kDbSQ1hiQFxqSBf2_DBaEHoyNvDpRQMFUvF_IUAwCDH2UMkEg_TxPqon1rNkkG49Xt2Rnz2Gu_yCeFQkjYEiKUJGkPDVQ4Py5cFRgHJgQIPu90mQJBxfae8D3D5OHsFZV0YWTB8og5AEyOBjFqpHIYftjqc4UtJJpPgfJrdm_FDt_0xk76a5_WIJd_Jam6E1uDoyzckutyA-rep2MqOj0Xg6RM1JppDm5WvTcpaVueZx7ZZOiM6MDxehayODyXE6kGVipu-LOgMJDp5pODEGkwUOrht81KLEEbeVbIWAoGhQVoC1vdaA"

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

