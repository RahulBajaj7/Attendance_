import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
DROPBOX_ACCESS_TOKEN = "sl.u.AFgmUvu0WPLGmxCu-KKb0YmssYE8ABQgbsJRx5rJI4WyWepAVp-0AGTaH4_ERdqCFjlFAc65TRcks1X8YXOTN-gIDvNAB-dTimLGBauI3UMolKIxiyti5CCYuPi4SPH4h6aMJvetBUQNkvdTB39gp4WSEM3GTDVdUNN6q7fC98l4A-ytuhFGItw_hQU8a0oS496iSFUpKZxOKr9q_daFgqLbyHkp2-M7R_mfVu_AKjkhfwIHapY06TvXK_8Uqrs5QSp44dpS0cxLozPNUb5DyS5xoMK_VCrEuBf8y-ZPBfRtTYtmM-xmicseew1IArHqwGRdy0ssRpiNXvJV_UM5E5yvBzIQXfxIJ75eDYUGITMJgYcY7aHf9EZPBYWwDsIYB19JcUIVrVAq-H1mANld0xbvPl8Ez7aj8yKJEjMkSkMG9uQqiQmdXe8LtjDGUezzGbEbhF0ZwEhfvQSooKwGyUGzocsTUsp5Y9tVeC4khZvchRsok7wnN4xO8n7rA1Ocv_yWXXYbm3mDC3EoGjEOKL_RUFyAxwB03WOEB8fjmYNwVDuchm_Jgh5E21zKz4DAZif_phqkcWePmMvK8yCaTe965zmUvamgOnOGEXO79fyppMuGAoAIrM7gyaahSBalGfInc-bWy6cYpfu6iSYKcrHSMQmp4aCBP_RZWym9Bw1Q6qD6qa54RdaGoqdcy2Q4dCuSVHvjmIq251pEZKzem7-ZRLL_zydzVC_SiNPoRBreWumCGdMYBPXO6lqVymBdbFIiAMk2bRWnO0RMC3Lq3h2trS10jpsBZ4v19czPa0s1TypEpJ2wNmUZe9Hz_16-fhLHzxYWYdD3QPeJ4NfM_nn7-E7VtD00Fx4U4t0ZzsBB70Doevw_8u83-9M3pTLKBteHhoDxIZ4PfOKIlCeZ0uwQp1r6H_LOWicVvDelF_40b93RVab5_-K5c_OD2EU3w1a140rXaUKtYhvqwsJXBdKY9_Kfg5RzGZ7auGJ_kiF4DO1iXK_OfrEnWxH533f0l3e4Q6OINTDj5FisOriCFZGdDNXbtivvJbllt_JqDqsHEWRNLa1tsFtgq7wlgrY5XRpnrjGa6VI66L8i66Saba7C29I-t6Grp8S_briJgjn1CqS0FjKmxECYyh9npxUheo6eKnDalkYSRGSerjrqq9VS3inHAwf8jxdzWLfjp39ChMXKME-BYCDkzC3Y4EHqjXkHHgM_Vv2dU8it_rg17yewTUmTGuGvAUf-cyOHCEVXU9MyPD6AEoTi--Zd1W5QsBp6ax26bYfN-U_rxWPa-jmvD2le0CrECW_kRmg5806tAO_g8ArOcwVF5GmON1QoHYKunN9aOodRhHffeMXnBh4AedvFgOhjCU6g5bGvGH9oDKnMYOjABxItj8-0SrSh0rr8Rbh_nbXZe8vv2RApQqqasudUQjBSeg8s5hUyD5EpPg"
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
        # Reload the attendance data after saving to ensure it's updated
        load_attendance()
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
