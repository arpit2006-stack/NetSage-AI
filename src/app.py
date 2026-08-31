import streamlit as st
import pandas as pd
from pathlib import Path
from engine import diagnose_case

# Set page to wide mode with a professional title
st.set_page_config(page_title="NetSage Diagnostic Console", layout="wide")

# Inject custom CSS for a cleaner, enterprise look (removing the standard Streamlit button vibe)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #005073;
        color: white;
        border-radius: 4px;
        font-weight: 500;
        border: none;
    }
    .stButton>button:hover {
        background-color: #003b54;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("NetSage Diagnostic Console")
st.caption("Operator Review & Network Troubleshooting Interface")

# Load data
csv_path = Path("data/cases.csv")
if not csv_path.exists():
    csv_path = Path("cases.csv")

if not csv_path.exists():
    st.error("System Error: cases.csv not found in data/ directory.")
    st.stop()

df = pd.read_csv(csv_path)

st.sidebar.header("Workspace")
selected_id = st.sidebar.selectbox("Select Active Incident", df["case_id"].tolist())
case_row = df[df["case_id"] == selected_id].iloc[0].to_dict()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Incident Details")
    st.markdown(f"**Case ID:** `{case_row['case_id']}`")
    st.markdown(f"**Reported Symptom:** {case_row['symptom']}")
    st.markdown(f"**Topology Context:** {case_row['topology_note']}")
    st.markdown(f"**Domain:** `{case_row['concept_tag']}` | **Severity:** `{case_row['severity']}`")
    
    st.subheader("CLI Telemetry")
    st.code(case_row['show_outputs'], language="bash")

# Run the backend engine
diagnosis = diagnose_case(case_row)

with col2:
    st.subheader("System Diagnosis")
    st.info(f"**Detected Root Cause:** {diagnosis['root_cause']}")
    
    m1, m2 = st.columns(2)
    m1.metric("Fault Layer", diagnosis["osi_layer"])
    m2.metric("Confidence Score", diagnosis["confidence"])
    
    st.markdown(f"**Supporting Evidence:** `{diagnosis['evidence']}`")
    st.markdown(f"**Next Verification Step:** `{diagnosis['next_command']}`")
    
    st.subheader("Proposed Remediation Plan")
    cmd_text = "\n".join(diagnosis["fix_steps"])
    st.text_area("Review and Modify CLI Commands:", value=cmd_text, height=100)
    
    st.subheader("Operator Decision Gate")
    b1, b2, b3 = st.columns(3)
    if b1.button("Approve & Deploy", use_container_width=True):
        st.success(f"Execution authorized for Incident {selected_id}.")
    if b2.button("Save Overrides", use_container_width=True):
        st.warning(f"Modified configuration saved for {selected_id}.")
    if b3.button("Reject Diagnosis", use_container_width=True):
        st.error(f"Incident {selected_id} flagged for manual review.")
