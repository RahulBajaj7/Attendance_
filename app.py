import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import dropbox
from dropbox.exceptions import AuthError, ApiError

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
DROPBOX_ACCESS_TOKEN = "sl.u.AFgCee1tA_4lFr-mDaqGECNr1Np5vHFo3WvZTLzKeWnjFxFCHbuIOKf_CBdVN1Mb0t14g-5p_QLnv2z6B_yl94xtuyS-CtFBweUnlqmX57tdCzMiJmediw2JFk6juhPgzef5QC8QaeUxCgFosgzMo3Yvk9S67iexxHbk7Wo5kXk59PmvYovIWgS57eo53odBP-zBLb_ZUwaLr7apW9hy3nTsmrd7rEKygR2ce7VJ562laAQ3xFg0zLd8zxpCLnBBe65OTbcCHKdnbpLhUd3lbyVwFUeAVNYaCYoV5txyXJwU2z9tChTIkx9Xrs8rwH7JW0FlutvAG-ZAY2dMg-_wG1H-CZAKTJOUnagyhX-gFeXUfe0hSbbrQCUf764plvvkrzO0QMIKKt14WS6j_DDJWbx1_scba3mNA_5a1j-yWIbEQnNuW5ArpU7lItQIe7SXAWUnVFwiC6c5lXgds25Fz7lnq3r9KThXmOEfYoD6m75SU42KoKK7X0Aj7Pt18jZkaZvikDB9L1aNXFGhsV8C35nXjHh1m_jv4zgjkqAWcHqz87mH2CD15NyjzCkTAaZPcK17A_8KjxcCpBGbuN5Dpz2QeeNnMtx14XVNhuel8TxH4Sh6g44trGozX_R32X_nw5ur9ym_jmsXjYjEh0bRBJihbPX9vkHyVp6nzJTg0T5V5gDLTHx866z_8fCW21lWBNkrc1kpfGxb-4IP1aH8xAKME2PE9EUgBn7DKoegCEcjHTtk7tZ5iXbA5oZJIyH_Xhe5QvNoiJfFF3g6L6RnYTOAmtgIYCFWft3g31RhAbAF1Ppnzk79E8VPgRhhRe1_oFofGC5aTkiGY6RtUPCEA83If70BncE7kbsSGbViE70VNyDncMD_JeG-DZZymQMrzcmFQ4ZlgaIKIufXo0Z7cKFVgpx_qxkA8Anuy7eusYO_ER52kTyWoTRxAD378B1fnxHMqtLerpimBa9BLqET3Nry2CVWuRidy850X-PBBmXNSPOUdzkCRuByst-vF713pkqtaSgMLbAvhBsFSrRGLLkVHsxvYyinu6teyWDcLULIdJ_2UZ_Ctf9dfd41SuyoXGLAlzQ-V7fVIoQnlTmXeUpK9LvAlbUuE7cx8Bzl7AJFsrUKXE5h1pIE1xch9iDrsB9rbEs4wf7-PnUYcNAw9AadJx31hkYTsfCCIP7yeI4BDjFwMeDJe_qgsegtWMBsbxjspUlkzcDMZELBDFUosZ_gH8_CrAj6tzA9w_HjeMFCQ2mx777xb5dPfYlR9CmyDWHwL1yk4__4omdNQNVHR-LVAHcLXGfNj9jWIX5bhUnh12Qtwnuj_LHN0T09krxsFmtVn7Ld3yg73th1xYuamPhfhQl8d7DHkmDatJ1SRC_Jh5gOSYamguhGLo6ZgaxF2NP_E5Wo-DkbDnlok7DrcDzeUbHEtKhupIE8PgmueVa0iw"
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
            st.error(f"Error loading attendance: {e}")

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
        response = dbx.files_upload(df.to_csv(index=False).encode(), DROPBOX_FOLDER_PATH + "/" + DROPBOX_FILE_NAME, mode=dropbox.files.WriteMode("overwrite"))
        st.success("Attendance data saved successfully to Dropbox!")
        st.write(response)  # Optional: Log the response for debugging
    except ApiError as api_error:
        if api_error.is_path() and api_error.get_path().is_conflict():
            st.error(f"Conflict error: {api_error}")
        else:
            st.error(f"API Error: {api_error}")
    except AuthError as auth_error:
        st.error(f"Authentication Error: {auth_error}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

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
