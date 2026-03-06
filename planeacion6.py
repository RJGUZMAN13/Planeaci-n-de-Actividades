# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:50:36 2026

@author: rjguz
"""

# gantt_15_weeks_professional.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Planning - Industrial Shield Predict AI (Executive)", layout="wide")

# Watermark in top-right corner with CSS (subtle)
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        top: 8px;
        right: 12px;
        opacity: 0.10;
        font-size: 16px;
        font-weight: 600;
        color: #444444;
        pointer-events: none;
        user-select: none;
        z-index: 9999;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* General background and typography */
    .main {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
    }
    /* Sidebar scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e1e1e;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #555;
        border-radius: 10px;
    }
    /* Buttons */
    button[kind="primary"] {
        background-color: #004080 !important;
        color: white !important;
        font-weight: 600;
    }
    /* Headings */
    h1, h2, h3 {
        font-weight: 700;
        color: #f0f0f0;
    }
    </style>
    <div class="watermark">Juan Rodrigo Guzmán Martínez</div>
    """,
    unsafe_allow_html=True
)

st.title("Activity Planning — Industrial Shield Predict AI")
st.markdown("15-week schedule (start date: 01-01-2026). Hover over bars for details.")

# Planning parameters
START_DATE = datetime(2026, 1, 1)
NUM_WEEKS = 15
END_DATE = START_DATE + timedelta(weeks=NUM_WEEKS) - timedelta(days=1)

# Task definitions with start week and duration in weeks
raw_tasks = [
    {"Phase": "Phase 1: Analysis and Survey", "Task": "Identification of critical equipment",
     "start_week": 1, "duration_weeks": 2,
     "Description": "On-site survey: robots, PLCs, conveyors, and welding systems.",
     "Deliverables": "Initial diagnostic document; Equipment map"},
    {"Phase": "Phase 1: Analysis and Survey", "Task": "Operational parameters survey",
     "start_week": 1, "duration_weeks": 3,
     "Description": "Measurement and recording: vibration, temperature, pressure, power consumption, cycles.",
     "Deliverables": "List of critical variables; Sensor placement points"},
    {"Phase": "Phase 1: Analysis and Survey", "Task": "Review of failure history",
     "start_week": 2, "duration_weeks": 3,
     "Description": "Analysis of unplanned stops and historical patterns.",
     "Deliverables": "Failure report and detected patterns"},
    {"Phase": "Phase 2: System Design", "Task": "Selection of IoT sensors",
     "start_week": 4, "duration_weeks": 2,
     "Description": "Selection of sensors for each critical variable.",
     "Deliverables": "Technical specifications of sensors"},
    {"Phase": "Phase 2: System Design", "Task": "Definition of communication architecture",
     "start_week": 4, "duration_weeks": 3,
     "Description": "Network design and protocol selection (Modbus TCP, OPC-UA, EtherNet/IP).",
     "Deliverables": "Communication diagram and topology"},
    {"Phase": "Phase 2: System Design", "Task": "Data flow design",
     "start_week": 5, "duration_weeks": 2,
     "Description": "Data flow from sensors/PLCs to the predictive platform.",
     "Deliverables": "System architecture diagrams"},
    {"Phase": "Phase 3: Predictive Software Development", "Task": "Implementation of AI algorithms",
     "start_week": 7, "duration_weeks": 3,
     "Description": "Anomaly detection, RUL, and time series models.",
     "Deliverables": "Trained models and test notebooks"},
    {"Phase": "Phase 3: Predictive Software Development", "Task": "Integration of sensor and machine data",
     "start_week": 7, "duration_weeks": 3,
     "Description": "ETL pipelines and continuous ingestion channels.",
     "Deliverables": "Data channels and pipelines"},
    {"Phase": "Phase 3: Predictive Software Development", "Task": "User interface development",
     "start_week": 8, "duration_weeks": 2,
     "Description": "Real-time alert dashboard and visualizations.",
     "Deliverables": "UI prototype / control panel"},
    {"Phase": "Phase 4: Integration with Control Systems", "Task": "Bidirectional communication setup",
     "start_week": 10, "duration_weeks": 2,
     "Description": "Secure connection with PLCs and robots (safe read/write).",
     "Deliverables": "Established connection and documentation"},
    {"Phase": "Phase 4: Integration with Control Systems", "Task": "Programming automatic actions",
     "start_week": 10, "duration_weeks": 3,
     "Description": "Logic blocks for parameter adjustment and controlled stops.",
     "Deliverables": "Control scripts/blocks and tests"},
    {"Phase": "Phase 4: Integration with Control Systems", "Task": "Safety validation",
     "start_week": 11, "duration_weeks": 2,
     "Description": "Functional safety tests before authorizing automatic actions.",
     "Deliverables": "Protocols and validation reports"},
    {"Phase": "Phase 5: Pilot Plant Testing", "Task": "Installation on pilot line",
     "start_week": 12, "duration_weeks": 1,
     "Description": "Physical installation of sensors and connections on pilot line.",
     "Deliverables": "System installed on pilot plant"},
    {"Phase": "Phase 5: Pilot Plant Testing", "Task": "Monitoring under real conditions",
     "start_week": 12, "duration_weeks": 3,
     "Description": "Monitoring KPIs and model adjustment in real environment.",
     "Deliverables": "Performance and KPI report"},
    {"Phase": "Phase 5: Pilot Plant Testing", "Task": "Final evaluation and adjustments",
     "start_week": 13, "duration_weeks": 2,
     "Description": "Final iterations based on pilot results.",
     "Deliverables": "List of improvements and iterations"},
    {"Phase": "Phase 6: Documentation and Replicability", "Task": "Preparation of technical manuals",
     "start_week": 14, "duration_weeks": 1,
     "Description": "Installation, operation, and maintenance manuals.",
     "Deliverables": "Complete technical manual"},
    {"Phase": "Phase 6: Documentation and Replicability", "Task": "Final report and scaling plan",
     "start_week": 14, "duration_weeks": 2,
     "Description": "Final project report and plan to replicate in other plants.",
     "Deliverables": "Final report and replicability plan"},
]

# Build DataFrame with calculated dates
tasks = []
for t in raw_tasks:
    start = START_DATE + timedelta(weeks=(t["start_week"] - 1))
    finish = start + timedelta(days=t["duration_weeks"] * 7 - 1)
    if finish > END_DATE:
        finish = END_DATE
    tasks.append({
        "Phase": t["Phase"],
        "Task": t["Task"],
        "Start": start,
        "Finish": finish,
        "Description": t["Description"],
        "Deliverables": t["Deliverables"]
    })

df = pd.DataFrame(tasks)

# Phase order for Y axis
phase_order = [
    "Phase 1: Analysis and Survey",
    "Phase 2: System Design",
    "Phase 3: Predictive Software Development",
    "Phase 4: Integration with Control Systems",
    "Phase 5: Pilot Plant Testing",
    "Phase 6: Documentation and Replicability"
]

# Phase filter
all_phases = df["Phase"].unique().tolist()
selected_phases = st.multiselect("Filter phases to display", options=all_phases, default=all_phases)

df_vis = df[df["Phase"].isin(selected_phases)].copy()
df_vis = df_vis.reset_index(drop=True)

# Week marks (top axis)
week_starts = [START_DATE + timedelta(weeks=i) for i in range(NUM_WEEKS)]
week_labels = [f"Week {i+1}" for i in range(NUM_WEEKS)]

# Month marks (bottom axis)
month_candidates = [datetime(2026, m, 1) for m in range(1, 13)]
month_starts = [m for m in month_candidates if START_DATE <= m <= END_DATE]
month_map = {"January":"January","February":"February","March":"March","April":"April",
             "May":"May","June":"June","July":"July","August":"August",
             "September":"September","October":"October","November":"November","December":"December"}
month_labels = [month_map[m.strftime("%B")] for m in month_starts]

# Vertical dotted lines for week start
shapes = []
for ws in week_starts:
    shapes.append(dict(
        type="line",
        x0=ws,
        y0=-0.5,
        x1=ws,
        y1=len(phase_order)-0.5,
        line=dict(color="#444444", width=1, dash="dot"),
        xref='x',
        yref='y'
    ))

# Create Plotly timeline figure with dark theme and dark tooltip
fig = px.timeline(
    df_vis,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Phase",
    hover_data=["Task", "Description", "Deliverables"],
    category_orders={"Phase": phase_order},
    color_discrete_sequence=px.colors.sequential.Plasma_r
)

fig.update_yaxes(autorange="reversed", title="Phases", gridcolor="#333333", tickfont=dict(color="#cccccc"))
fig.update_layout(
    height=720,
    margin=dict(l=220, r=40, t=120, b=120),
    showlegend=False,
    plot_bgcolor="#121212",
    paper_bgcolor="#121212",
    font=dict(family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", size=13, color="#e0e0e0"),
    hoverlabel=dict(
        bgcolor="#222222",
        font_size=13,
        font_family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        font_color="#f0f0f0",
        bordercolor="#555555"
    ),
    title=dict(text=f"Schedule — {NUM_WEEKS} weeks (01-01-2026 to {END_DATE.strftime('%d-%m-%Y')})", x=0.5, font=dict(size=22, color="#f0f0f0")),
    shapes=shapes,
    xaxis=dict(
        tickvals=week_starts,
        ticktext=week_labels,
        tickangle=0,
        tickfont=dict(size=11, color="#bbbbbb"),
        range=[START_DATE, END_DATE],
        title="Weeks (top)",
        side="top",
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='#444444',
        domain=[0, 1]
    ),
    xaxis2=dict(
        tickvals=month_starts,
        ticktext=month_labels,
        tickangle=0,
        tickfont=dict(size=15, color='#dddddd', family="'Segoe UI Black', Tahoma, Geneva, Verdana, sans-serif"),
        anchor='y',
        overlaying='x',
        side='bottom',
        showgrid=False,
        zeroline=False,
        showline=False,
        domain=[0, 1]
    )
)

st.plotly_chart(fig, use_container_width=True)

# Elegant sidebar
st.sidebar.header("📋 Control Panel and Details")
st.sidebar.markdown(
    """
    **Quick instructions:**  
    - Filter phases with the main selector (above the list).  
    - Select a numbered task to see its description and deliverables.  
    - Download the schedule as CSV or PNG (PNG requires `kaleido`).  
    - Hover over bars to see more information.
    """
)

task_list = df_vis["Task"].tolist()
task_list_num = [f"{i+1}. {task}" for i, task in enumerate(task_list)]

selected_task_num = st.sidebar.selectbox("🔍 Select a task (numbered)", options=["-- None --"] + task_list_num)

if selected_task_num and selected_task_num != "-- None --":
    try:
        idx = int(selected_task_num.split(".")[0]) - 1
        row = df_vis.iloc[idx]
        st.sidebar.markdown(f"### {row['Task']}")
        st.sidebar.markdown(f"**Phase:** {row['Phase']}")
        st.sidebar.markdown(f"**Start:** {row['Start'].date()}  \n**End:** {row['Finish'].date()}")
        st.sidebar.markdown("**Description:**")
        st.sidebar.write(row["Description"])
        st.sidebar.markdown("**Deliverables:**")
        st.sidebar.write(row["Deliverables"])
    except Exception:
        st.sidebar.error("Error selecting the task. Try reloading the page or updating the filter.")

st.sidebar.markdown("---")

csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("⬇️ Download schedule (CSV)", csv, "schedule_15_weeks_professional.csv", "text/csv")

if st.sidebar.button("⬇️ Download schedule (PNG)"):
    try:
        img_bytes = fig.to_image(format="png", width=1400, height=800, scale=2)
        st.sidebar.download_button("Download PNG image", img_bytes, "schedule_15_weeks_professional.png", "image/png")
    except Exception as e:
        st.sidebar.error("Could not export image to PNG from the server.")
        st.sidebar.markdown("To enable PNG export, install 'kaleido' in your environment and restart the app:")
        st.sidebar.code("pip install --upgrade kaleido")
        with st.sidebar.expander("Technical details (error)"):
            st.sidebar.write(str(e))

st.markdown("### 📝 Notes / Legend")
st.markdown(f"- Schedule starting on **{START_DATE.strftime('%d-%m-%Y')}** with a duration of **{NUM_WEEKS} weeks** (until {END_DATE.strftime('%d-%m-%Y')}).")
st.markdown("- Week labels are on the top row and months on the bottom row.")
st.markdown("- Dotted vertical lines mark the start of each week.")
st.markdown("- Select numbered tasks in the sidebar to view their description and deliverables.")