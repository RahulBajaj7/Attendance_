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

# Donut Chart with Adjusted Layout
fig = px.pie(
    names=["Earned Points", "Remaining Points"],
    values=[total_points, remaining_points],
    hole=0.5,
    color_discrete_sequence=["#1ABC9C", "#E74C3C"],  # Green & Red
)

fig.update_layout(
    title_text="📊 Seminar Points Progress",
    title_x=0.5,
    margin=dict(l=20, r=20, t=40, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    height=350
)

# Set Page Title
st.markdown("""
    <h1 style='text-align: center; color: #16A085;'>📊 Rahul & Tanu's Seminar Points 🎓👩‍❤️‍💋‍👨</h1>
""", unsafe_allow_html=True)

# Display Summary at Top
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-around; padding: 10px;">
        <div style="border: 3px solid #16A085; padding: 15px; border-radius: 10px; background-color: #1ABC9C; color: white; font-size: 18px; text-align: center;">
            ✅ <b>Total Points Earned:</b> <br> <span style='color: #F7DC6F; font-size: 24px;'><b>{total_points}</b></span>
        </div>
        <div style="border: 3px solid #E74C3C; padding: 15px; border-radius: 10px; background-color: #C0392B; color: white; font-size: 18px; text-align: center;">
            ❗ <b>Points Needed to Reach Goal:</b> <br> <span style='color: #F7DC6F; font-size: 24px;'><b>{remaining_points}</b></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Create Two Columns (Chart on Left, Table on Right)
col1, col2 = st.columns([1.5, 2])

# Left Column → Donut Chart
with col1:
    st.markdown("### 📈 Progress Toward 40 Points Goal")
    st.plotly_chart(fig, use_container_width=True)

# Right Column → Seminar Table
with col2:
    st.markdown("### 📅 Seminars Attended")
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
    st.write(df.style.set_properties(**{
        'background-color': '#1F2833',
        'color': 'white',
        'border-color': 'white',
        'text-align': 'center'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#16A085'), ('color', 'white'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ]))

