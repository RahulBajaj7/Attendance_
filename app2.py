import streamlit as st
import pandas as pd
import plotly.express as px

# Customizing Streamlit page
st.set_page_config(page_title="Rahul & Tanu's Seminar Points", layout="wide")

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
    {"Date": "16th January, 2025", "Topic": "Technovate: Design Thinking", "Points": 2},
    {"Date": "21st January, 2025", "Topic": "Technovate: Flutter Workshop", "Points": 2},
    {"Date": "30th January, 2025", "Topic": "Think Tank: Consulting", "Points": 2},
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Panel Discussion, Envision 1.0", "Points": 3},
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Real Talk Trailblazers, Envision 1.0", "Points": 3},
    {"Date": "01st February, 2025", "Topic": "Mastering Management 6", "Points": 2},
]

df = pd.DataFrame(data)

# Calculate total and remaining points
total_points = df["Points"].sum()
goal = 40
remaining_points = max(goal - total_points, 0)

# Donut Chart with Soft Colors
fig = px.pie(
    names=["Earned Points", "Remaining Points"],
    values=[total_points, remaining_points],
    hole=0.5,
    color_discrete_sequence=["#3498DB", "#E74C3C"]  # Blue & Red
)
fig.update_layout(title_text="📊 Seminar Points Progress", title_x=0.5)

# --- Streamlit App Layout ---
st.markdown(
    """
    <style>
        body {
            background-color: #1E1E1E;
            color: white;
        }
        .main {
            background-color: #1E1E1E;
            color: white;
        }
        .summary-container {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-top: 20px;
        }
        .summary-box {
            border: 2px solid #FFFFFF;
            background-color: #2C3E50;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 20px;
            color: white;
            font-weight: bold;
            width: 40%;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
        }
        .title {
            font-size: 34px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 22px;
            font-weight: bold;
            color: white;
            margin-top: 40px;
            text-align: center;
        }
        .dataframe-container {
            display: flex;
            justify-content: center;
        }
        table {
            margin: auto;
            border-collapse: collapse;
            width: 80%;
        }
        th, td {
            padding: 12px;
            border: 1px solid #FFFFFF;
            text-align: center;
            color: white;
        }
        th {
            background-color: #2C3E50;
        }
        tr:nth-child(even) {
            background-color: #34495E;
        }
        tr:nth-child(odd) {
            background-color: #2C3E50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title">Rahul & Tanu\'s Seminar Points 🎓📊</div>', unsafe_allow_html=True)

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

# Modify DataFrame to include Serial Number starting from 1
df.index = range(1, len(df) + 1)  # Start index from 1
df.index.name = "S.No"

# Display Seminar Data (Centered & Styled)
st.markdown('<div class="section-header">📅 Seminars Attended</div>', unsafe_allow_html=True)
st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
st.write(df.style.set_properties(**{
    'background-color': '#2C3E50',
    'color': 'white',
    'border-color': 'white',
    'text-align': 'center'
}).set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#2C3E50'), ('color', 'white'), ('text-align', 'center')]},
    {'selector': 'td', 'props': [('text-align', 'center')]}
]))
st.markdown('</div>', unsafe_allow_html=True)
