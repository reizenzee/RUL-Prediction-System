# =====================================================
# POWER GRID ASSET RUL PREDICTION SYSTEM
# =====================================================

import streamlit as st
import pandas as pd
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Power Grid Asset RUL Prediction",
    page_icon="⚡",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(
    "models/tuned_xgboost.pkl"
)

# =====================================================
# CUSTOM HEADER
# =====================================================

st.title("⚡ RUL Prediction")

st.markdown("Predict remaining useful life of power grid assets")

# =====================================================
# INPUTS
# =====================================================

with st.expander("Asset Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        asset_type = st.selectbox(
            "Asset Type",
            [
                "Transformer",
                "Circuit Breaker",
                "Cable",
                "Recloser",
                "Switchgear"
            ]
        )
    with col2:
        condition_score = st.number_input(
            "Condition Score",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=0.1
        )
    
    col3, col4 = st.columns(2)
    with col3:
        total_maintenance_cost = st.number_input(
            "Total Maintenance Cost",
            min_value=0.0,
            value=5000.0,
            step=100.0
        )
    with col4:
        failure_impact_score = st.number_input(
            "Failure Impact Score",
            min_value=1,
            max_value=100,
            value=50,
            step=1
        )

with st.expander("Operational Data", expanded=True):
    col5, col6 = st.columns(2)
    with col5:
        failure_history_count = st.number_input(
            "Failure History Count",
            min_value=0,
            value=1,
            step=1
        )
    with col6:
        operating_hours = st.number_input(
            "Operating Hours",
            min_value=0,
            value=10000,
            step=100
        )
    
    col7, col8 = st.columns(2)
    with col7:
        days_since_maintenance = st.number_input(
            "Days Since Maintenance",
            min_value=0,
            value=180,
            step=1
        )
    with col8:
        failure_probability = st.number_input(
            "Failure Probability",
            min_value=0.01,
            max_value=0.99,
            value=0.50,
            step=0.01
        )

with st.expander("System Parameters"):
    col9, col10 = st.columns(2)
    with col9:
        environmental_stress_index = st.number_input(
            "Environmental Stress Index",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    with col10:
        system_importance_score = st.number_input(
            "System Importance Score",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    
    budget_constraint_flag = st.selectbox(
        "Budget Constraint Flag",
        [0, 1]
    )

# =====================================================
# CREATE INPUT DATAFRAME
# =====================================================

input_data = pd.DataFrame({
    'Asset_Type': [asset_type],
    'Total_Maintenance_Cost': [total_maintenance_cost],
    'Condition_Score': [condition_score],
    'Failure_Impact_Score': [failure_impact_score],
    'Failure_History_Count': [failure_history_count],
    'Operating_Hours': [operating_hours],
    'Environmental_Stress_Index': [environmental_stress_index],
    'System_Importance_Score': [system_importance_score],
    'Budget_Constraint_Flag': [budget_constraint_flag],
    'Days_Since_Maintenance': [days_since_maintenance],
    'Failure_Probability': [failure_probability]
})

# =====================================================
# MAIN CONTENT
# =====================================================

predict_button = st.button("Predict RUL", use_container_width=True, type="primary")

if predict_button:
    prediction = model.predict(input_data)
    predicted_rul = prediction[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted RUL", f"{predicted_rul:.2f} years")
    
    with col2:
        if predicted_rul < 3:
            risk = "🔴 High"
        elif predicted_rul < 7:
            risk = "🟡 Medium"
        else:
            risk = "🟢 Low"
        st.metric("Risk Level", risk)
    
    with col3:
        priority = "Urgent" if predicted_rul < 3 else ("Moderate" if predicted_rul < 7 else "Low")
        st.metric("Priority", priority)
    
    with st.expander("View Details"):
        st.dataframe(input_data, use_container_width=True)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Developed using Streamlit, XGBoost, and Machine Learning for Power Grid Asset RUL Prediction"
)