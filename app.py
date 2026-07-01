import streamlit as st
import pandas as pd
import plotly.express as px

# Configure production page presentation layer
st.set_page_config(page_title="AI Emergency Department Intelligence Hub", layout="wide")

# Custom CSS styling injection to create a sleek, professional interface
st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #ffffff; }
    .stMetric { background-color: #1e222b; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI-Driven Emergency Department Workload & Triage Dashboard")
st.subheader("Operational Predictive Insights Engine | Fordham Clinical Informatics Strategy")
st.markdown("---")

# Load our production CSV data matrix safely
@st.cache_data
def load_hospital_data():
    df = pd.read_csv("er_patient_data.csv")
    df["Arrival_Timestamp"] = pd.to_datetime(df["Arrival_Timestamp"])
    return df

try:
    df = load_hospital_data()
except FileNotFoundError:
    st.error("Data layer file 'er_patient_data.csv' not found. Please run the data synthesizer script first.")
    st.stop()

# ==================== SIDEBAR FILTER SYSTEM ====================
st.sidebar.header(" Clinical Search Filters")
selected_symptom = st.sidebar.multiselect(
    "Filter by Patient Chief Complaint:",
    options=df["Chief_Complaint"].unique(),
    default=df["Chief_Complaint"].unique()
)

selected_zone = st.sidebar.selectbox(
    "Select Target Operational ER Zone:",
    options=["All Zones"] + list(df["Triage_Zone"].unique())
)

# Apply dynamic matrix filtering logic based on sidebar user state
filtered_df = df[df["Chief_Complaint"].isin(selected_symptom)]
if selected_zone != "All Zones":
    filtered_df = filtered_df[filtered_df["Triage_Zone"] == selected_zone]

# ==================== KEY METRIC CHARTS LAYOUT ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Patient Volume Logged", f"{len(filtered_df):,}")
with col2:
    avg_wait = filtered_df["Wait_Time_Minutes"].mean()
    st.metric("Average ER Wait Time", f"{avg_wait:.1f} Mins", delta=f"{avg_wait - 45:.1f} vs Target")
with col3:
    avg_hr = filtered_df["Heart_Rate_BPM"].mean()
    st.metric("Mean Physiological Heart Rate", f"{avg_hr:.1f} BPM")
with col4:
    critical_cases = len(filtered_df[filtered_df["Heart_Rate_BPM"] > 120])
    st.metric("Active High-Risk Anomalies", f"{critical_cases:,} Cases")

st.markdown("---")

# ==================== DATA SCIENCE VISUALIZATIONS ====================
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader(" Case Allocation by Chief Complaint")
    complaint_counts = filtered_df["Chief_Complaint"].value_counts().reset_index()
    complaint_counts.columns = ["Chief Complaint", "Total Logs"]
    
    fig_pie = px.pie(
        complaint_counts, 
        values="Total Logs", 
        names="Chief Complaint", 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pie.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader(" Wait Time Variance Mapping (Resource Vulnerability)")
    fig_bar = px.bar(
        filtered_df.groupby("Chief_Complaint")["Wait_Time_Minutes"].mean().reset_index(),
        x="Chief_Complaint",
        y="Wait_Time_Minutes",
        labels={"Chief_Complaint": "Declared Symptom Vector", "Wait_Time_Minutes": "Mean Wait Duration (Min)"},
        color="Wait_Time_Minutes",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_bar.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

# ==================== STREAMING DATA OBSERVATION LEDGER ====================
st.subheader(" Live Emergency Department Data Stream (10,000 Vectors)")
st.dataframe(filtered_df.sort_values(by="Arrival_Timestamp", ascending=False).head(100), use_container_width=True)