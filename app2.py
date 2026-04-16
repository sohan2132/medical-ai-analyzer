import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

from pipeline import run_pipeline


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Medical Report Analyzer")


# ---------------- RISK GAUGE FUNCTION ----------------
def show_risk_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Health Risk Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 20], 'color': "green"},
                {'range': [20, 50], 'color': "yellow"},
                {'range': [50, 100], 'color': "red"}
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)


# ---------------- FILE UPLOAD ----------------
st.subheader("Upload Medical Report")

uploaded_file = st.file_uploader(
    "Upload PDF or Image",
    type=["pdf", "jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    # Save uploaded file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    if st.button("Run Analysis"):

        with st.spinner("Running AI pipeline..."):

            result = run_pipeline(uploaded_file.name)

        if result is not None:

            data = result["data"]
            score = result["score"]
            decision = result["decision"]

            st.divider()

            # -------- EXTRACTED DATA --------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Extracted Medical Data")
                st.json(data)

            # -------- RISK GAUGE --------
            with col2:
                st.subheader("Risk Score")
                show_risk_gauge(score)

            st.divider()

            # -------- POLICY DECISION --------
            st.subheader("Policy Decision")

            if score < 20:
                st.success(decision)
            elif score < 50:
                st.warning(decision)
            else:
                st.error(decision)


# ---------------- DATABASE VIEWER ----------------
st.divider()
st.subheader("Processed Medical Reports")

try:

    conn = sqlite3.connect("medical_reports.db")

    df = pd.read_sql_query("SELECT * FROM reports", conn)

    conn.close()

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No reports processed yet.")

except:
    st.warning("Database not found yet.")