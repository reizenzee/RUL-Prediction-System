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
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:
    st.markdown("## Navigation")
    
    nav_option = st.radio(
        "Select Section",
        ["Asset Prediction", "Prediction History", "Batch Analysis"],
        label_visibility="collapsed"
    )

# =====================================================
# MAIN CONTENT
# =====================================================

if nav_option == "Asset Prediction":
    st.title("RUL Prediction Form")
    
    st.markdown("### Asset Information")
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
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
    
    with col3:
        total_maintenance_cost = st.number_input(
            "Total Maintenance Cost ($)",
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
    
    st.markdown("### Operational Data")
    col5, col6, col7, col8 = st.columns(4, gap="small")
    
    with col5:
        operating_hours = st.number_input(
            "Operating Hours",
            min_value=0,
            value=10000,
            step=100
        )
    
    with col6:
        failure_history_count = st.number_input(
            "Failure History Count",
            min_value=0,
            value=1,
            step=1
        )
    
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
    
    st.markdown("### System Parameters")
    col9, col10, col11 = st.columns(3, gap="small")
    
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
    
    with col11:
        budget_constraint_flag = st.selectbox(
            "Budget Constraint",
            ["No", "Yes"]
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
        'Budget_Constraint_Flag': [1 if budget_constraint_flag == "Yes" else 0],
        'Days_Since_Maintenance': [days_since_maintenance],
        'Failure_Probability': [failure_probability]
    })
    
    # =====================================================
    # PREDICTION
    # =====================================================
    
    st.markdown("---")
    st.button("🔮 Predict RUL", use_container_width=True, key="predict_btn")
    
    if st.session_state.get("predict_btn"):
        prediction = model.predict(input_data)
        predicted_rul = prediction[0]
        
        st.markdown("---")
        st.markdown("### Prediction Result")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric("Predicted RUL", f"{predicted_rul:.2f} years")
        
        with res_col2:
            if predicted_rul < 3:
                risk = "🔴 High"
            elif predicted_rul < 7:
                risk = "🟡 Medium"
            else:
                risk = "🟢 Low"
            st.metric("Risk Level", risk)
        
        with res_col3:
            priority = "Urgent" if predicted_rul < 3 else ("Moderate" if predicted_rul < 7 else "Low")
            st.metric("Priority", priority)
        
        with st.expander("📊 View Input Data"):
            st.dataframe(input_data, use_container_width=True)

elif nav_option == "Prediction History":
    st.title("Prediction History")
    st.info("View your previous RUL predictions and analysis results.")

elif nav_option == "Batch Analysis":
    st.title("Batch Analysis")
    st.markdown("Upload a CSV file to predict RUL for multiple assets at once.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.markdown("### Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        if st.button("🔮 Predict for All Assets", use_container_width=True):
            try:
                predictions = model.predict(df)
                df['Predicted_RUL'] = predictions
                
                st.markdown("### Results")
                st.dataframe(df, use_container_width=True)
                
                # Download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results",
                    data=csv,
                    file_name="rul_predictions.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")