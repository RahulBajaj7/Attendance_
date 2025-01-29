import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ... (rest of your code: subject details, file path, load/save functions)

# Attendance Input Section
st.subheader("📌 Mark Attendance")
for subject, max_classes in subjects.items():
    st.write(f"### {subject} (Max: {max_classes})")

    conducted_key = f"{subject}_conducted"

    if conducted_key not in st.session_state:
        st.session_state[conducted_key] = len(st.session_state.attendance.get(subject, []))

    conducted = st.number_input(
        f"Sessions Conducted for {subject}",
        min_value=0,
        max_value=max_classes,
        value=st.session_state[conducted_key],
        step=1,
        key=conducted_key
    )

    # TRUNCATE or PAD the attendance list based on 'conducted'
    st.session_state.attendance[subject] = st.session_state.attendance[subject][:conducted] # Truncate
    while len(st.session_state.attendance[subject]) < conducted: # Pad
        st.session_state.attendance[subject].append(False)  # Pad with False (Absent)

    for i in range(conducted):
        session_key = f"{subject}session{i+1}"
        if session_key not in st.session_state:
            st.session_state[session_key] = st.session_state.attendance[subject][i] if i < len(st.session_state.attendance[subject]) else False

        st.session_state.attendance[subject][i] = st.checkbox(
            f"Session {i+1}",
            value=st.session_state[session_key],
            key=session_key
        )

# ... (rest of your code: summary table)

# Save attendance data when button is clicked
if st.button("💾 Save Attendance"):
    # Ensure all subjects have the same number of entries (padding) before saving.
    max_length = max(len(lst) for lst in st.session_state.attendance.values())
    for subject in subjects:
        while len(st.session_state.attendance[subject]) < max_length:
            st.session_state.attendance[subject].append(False)  # Pad with False

    save_attendance()  # Your existing save_attendance function
    st.success("Attendance data saved successfully!")
