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
    {"Date": "16th January, 2025", "Topic": "Technovate: Design Thinking", "Points": 2},
    {"Date": "21st January, 2025", "Topic": "Technovate: Flutter Workshop", "Points": 2},
    {"Date": "30th January, 2025", "Topic": "Think Tank: Consulting", "Points": 2},
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Panel Discussion, Envison 1.0", "Points": 3},
    {"Date": "31st January, 2025", "Topic": "Oraculum 2025: Real Talk Trailblazers, Envison 1.0", "Points": 3},
    {"Date": "01st February, 2025", "Topic": "Mastering Management 6", "Points": 2},
    {"Date": "22nd February, 2025", "Topic": "Leadership Luminaries: B2B Sales", "Points": 2},
]

df = pd.DataFrame(data)

# Add Serial Number
df.index = range(1, len(df) + 1)
df.index.name = "S.No"

# Calculate points
total_points = df["Points"].sum()
goal = 40
remaining_points = max(goal - total_points, 0)

# Donut Chart with Minimalist Style
fig = px.pie(
    names=["Earned", "Remaining"],
    values=[total_points, remaining_points],
    hole=0.6,
    color_discrete_sequence=["#2ECC71", "#E74C3C"],
)

fig.update_layout(
    title_text="Progress to Goal",
    title_x=0.5,
    margin=dict(l=20, r=20, t=40, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    height=320
)

# Page Title
st.title("📊 Seminar Points Tracker")

# Summary Section
st.markdown(
    f"""
    <div style="text-align: center; padding: 10px;">
        <h2 style="color: #2C3E50;">Total Points: <span style='color: #2ECC71;'>{total_points}</span></h2>
        <h3 style="color: #2C3E50;">Remaining: <span style='color: #E74C3C;'>{remaining_points}</span></h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Layout
col1, col2 = st.columns([1.2, 2])

# Left Column → Donut Chart
with col1:
    st.plotly_chart(fig, use_container_width=True)

# Right Column → Seminar Table
with col2:
    st.markdown("### 📅 Seminars Attended")
    st.write(df.style.set_properties(**{
        'background-color': '#F4F6F6',
        'color': '#2C3E50',
        'border-color': '#D5D8DC',
        'text-align': 'center'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#2ECC71'), ('color', 'white'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ]))
