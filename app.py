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
DROPBOX_ACCESS_TOKEN = "sl.u.AFjqrbQzPg7R4joM8k5anKdSSHMxLu1IAR1UJQj5rYBWKQQ-NpJnremJ3JTpi7OZzjxJtKDe2c-SnQrs_Yj1WWCL1mLaglaghaGyyt9BXWnmP1Vb4yzD7bV8BcIohAXXIBhijacT8XRGIo0fIYv22AAfwp1FipW_jASizMMWEsVoIu-5xMXj8K89mnINZRvglIWQdAm_8TWJfAINjakSbL-Gi2vM5RK1VIhk-y9VbgGc6Mz15nKYysi5OByFYFzQBhYke_dUPlX_7o4z677sIMUz4Lfyr2QTjyQuSui6PSG8X4UJwh_1v7ftqEFV2XuLYGeom1FWGyTf_f79MQAqGWX8R_P4PeoFVl7qdPhHkjXGwYCJs5i2EbyW-0OfAdpsqbmm2-Wgpyn6o7rmyXU0fvBToBVndTK7FdaMR-G3I5NLlgwepPh8yv779s0GH5XOA-xDSCrUkNMexQCqNUWCFfld2l3VFJwzYkNTzyio9uyc2qH7a-etRgDPn3AoLVOs8MZAJhhQU_C9FJigQjjF5bB26k7kpX2Ojzw78dYXhmncIHU2IMDhtFiH80-wvtIXsl0EwarskniyDWC8lPIU8zkyCR5XzN9xsY4Npoao8NHqE1TRW6nKAgWHpwhxdNzvph5uqEhZabUlkpxQBly7W7tm-AysGtMpRESPlnpDw5_XbvsDYbOVYGgkwT8j-D3P7TXM1Lf0_8h_n_qtLpuMq8zeQoARZHwtZtsYch8khIrbKXsny8XGrNn4kiqdCwaHwl8NJ4V6q9GItfSsCDqrbhM9u1HAxCaG_IQ6jvemVJ4_4kEwb4YEA5bbTxv_XpOJn2x8ju4BnEURYZ0CelBrwlAJ7Gg0L_HZURAbmocoGZZTUq2rSHI8UPb1VKMs23x1OMO7FBAHBITZqQhN6zlHN85z9abHv1Y0u25Z6yX1FXRK9A5_mH8CoDoDF_2LH9kSZIRgOF910EDqGitVHdfC2Ex7MxN9eNdM_6c7I12u_mkqWdgbya9IM89ARSBw2QArKt-8fi9DAi9Vo9eqtnwKd1_ua8Kk3i52APOcK-J9vkClNU1m0S-C0_yTMlNpUF4GrnO6ZVmtDmosv-AN-BFNzVuKGvsTu-KABli_lE4SoVjgYl3TaVReZxB_fVc9OnYTNZHAGWsSbaJ0d2B6_tVBbY9POrNNhZ5Jqcer7LdVDog5RNG9CNBhrPqAyzbVPXZEJ765Z-xELCXFpNZsOYIUpVDCWcAFwdnDJuu2MqnurkbLgpzjVfsDyZa7aToOXq2vcGyNe2yMl2KcWVNH-vZvOLU76BxprtwS2RRPgUDv3ToSs5xhozKQqk2G_Z_7mbZBi8h8hRGQA7Km2WnBxotJ6JAkS46G2nbofpuIHj2fb7JewwrcETU-UbyPN4QQYm4Jmndqx1tc2SYOakfC5Hc6Pa8KHHEFHUgl2K-aCiwnv3aUpA"
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
