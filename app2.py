import streamlit as st
import pandas as pd
import plotly.express as px

# Customizing Streamlit page
st.set_page_config(page_title="Seminar Attendance Tracker", layout="wide")

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
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Panel Discussion, Envison 1.0", "Points": 3},
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Real Talk Trailblazers, Envison 1.0", "Points": 3},
    {"Date": "01st February, 2025", "Topic": "Mastering Management 6", "Points": 2},
]

df = pd.DataFrame(data)

# Calculate total and remaining points
total_points = df["Points"].sum()
goal = 40
remaining_points = max(goal - total_points, 0)

# Donut Chart with Soothing Colors
fig = px.pie(
    names=["Earned Points", "Remaining Points"],
    values=[total_points, remaining_points],
    hole=0.5,
    color_discrete_sequence=["#5DADE2", "#F1948A"]  # Soft Blue & Light Coral Red
)
fig.update_layout(title_text="📊 Seminar Points Progress", title_x=0.5)

# --- Streamlit App Layout ---
st.markdown(
    """
    <style>
        .main {
            background-color: #F7F9F9;
        }
        .summary-container {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .summary-box {
            border: 2px solid #1E8449;
            background-color: #D5F5E3;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            color: #1E8449;
            font-weight: bold;
            width: 45%;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .title {
            font-size: 26px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 30px;
        }
        .section-header {
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
            margin-top: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title">📌 Seminar Attendance Tracker</div>', unsafe_allow_html=True)

# Summary Section
st.markdown('<div class="section-header">🌟 Progress Summary</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="summary-container">
        <div class="summary-box">📈 Total Points Earned: {total_points}</div>
        <div class="summary-box">🎯 Points Needed to Reach Goal: {remaining_points}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Donut Chart
st.markdown('<div class="section-header">📊 Progress Toward 40 Points Goal</div>', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)

# Display Seminar Data
st.markdown('<div class="section-header">📅 Seminars Attended</div>', unsafe_allow_html=True)
st.dataframe(df, hide_index=True)
