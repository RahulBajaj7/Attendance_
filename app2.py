import streamlit as st
import pandas as pd
import plotly.express as px

# Updated seminar data
data = [
    {"Date": "30th July, 2024", "Topic": "Invite for MOU Signing Ceremony with ClarityX, Mumbai", "Points": 2},
    {"Date": "2nd August, 2024", "Topic": "CID", "Points": 2},
    {"Date": "5th August, 2024", "Topic": "EBSCO Business Source Elite and ABI/INFORM Complete Database", "Points": 2},
    {"Date": "12th August, 2024", "Topic": "CMIE Prowess IQ and Eikon - Refinitiv Database", "Points": 3},
    {"Date": "11th September, 2024", "Topic": "Understanding Financial Behaviour & Financial Goal Setting", "Points": 2},
    {"Date": "29th November, 2024", "Topic": "FIMC", "Points": 2},
    {"Date": "30th November, 2024", "Topic": "FIMC", "Points": 2},
    {"Date": "16th December, 2024", "Topic": "CSD", "Points": 2},
    {"Date": "16th January, 2025", "Topic": "Technovate: Design Thinking)", "Points": 2},
    {"Date": "21st January, 2025", "Topic": "Technovate:Flutter Workshop", "Points": 2},
    {"Date": "30th January, 2025", "Topic": "Think Tank: Consulting", "Points": 2},
]

df = pd.DataFrame(data)

total_points = df["Points"].sum()
goal = 40
remaining_points = max(goal - total_points, 0)

# Donut Chart
fig = px.pie(
    names=["Earned Points", "Remaining Points"],
    values=[total_points, remaining_points],
    hole=0.5,
    color_discrete_sequence=["#E74C3C", "#3498DB"]  # Updated colors (blue & red)
)
fig.update_layout(title_text="Seminar Points Progress", title_x=0.5)

# Streamlit App
st.title("Seminar Attendance Tracker")

# Display Seminar Data
st.subheader("Seminars Attended")
st.dataframe(df, hide_index=True)

# Display Donut Chart
st.subheader("Progress Toward 40 Points Goal")
st.plotly_chart(fig)

# Display Summary
st.markdown(f"**Total Points Earned:** {total_points}")
st.markdown(f"**Points Needed to Reach Goal:** {remaining_points}")
