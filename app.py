
from database.database import (
    conn,
    cursor
)
# =====================================================
# POWER GRID ASSET RUL PREDICTION SYSTEM
# =====================================================

import random
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
    col_title, col_random = st.columns([3, 1])

    with col_title:
        st.title("RUL Prediction Form")

    asset_type_options = [
        "Transformer",
        "Circuit Breaker",
        "Cable",
        "Recloser",
        "Switchgear"
    ]

    def randomize_input_data():
        st.session_state["asset_type"] = random.choice(asset_type_options)
        st.session_state["condition_score"] = round(random.uniform(1.0, 10.0), 1)
        st.session_state["total_maintenance_cost"] = round(random.uniform(0.0, 100000.0), 2)
        st.session_state["failure_impact_score"] = random.randint(1, 100)
        st.session_state["operating_hours"] = random.randint(0, 20000)
        st.session_state["failure_history_count"] = random.randint(0, 10)
        st.session_state["days_since_maintenance"] = random.randint(0, 365)
        st.session_state["failure_probability"] = round(random.uniform(0.01, 0.99), 2)
        st.session_state["environmental_stress_index"] = round(random.uniform(0.1, 1.0), 1)
        st.session_state["system_importance_score"] = round(random.uniform(0.0, 1.0), 1)
        st.session_state["budget_constraint_flag"] = random.choice(["No", "Yes"])

    with col_random:
        st.button(
            "🎲 Randomize Input Data",
            use_container_width=True,
            key="randomize_btn",
            on_click=randomize_input_data
        )

    st.markdown("### Asset Information")
    col1, col2, col3, col4 = st.columns(4, gap="small")

    with col1:
        asset_type = st.selectbox(
            "Asset Type",
            asset_type_options,
            index=asset_type_options.index(
                st.session_state.get("asset_type", asset_type_options[0])
            ),
            key="asset_type"
        )

    with col2:
        condition_score = st.number_input(
            "Condition Score",
            min_value=1.0,
            max_value=10.0,
            value=st.session_state.get("condition_score", 1.0),
            step=0.1,
            key="condition_score"
        )

    with col3:
        total_maintenance_cost = st.number_input(
            "Total Maintenance Cost ($)",
            min_value=0.0,
            value=st.session_state.get("total_maintenance_cost", 0.0),
            step=100.0,
            key="total_maintenance_cost"
        )

    with col4:
        failure_impact_score = st.number_input(
            "Failure Impact Score",
            min_value=1,
            max_value=100,
            value=st.session_state.get("failure_impact_score", 1),
            step=1,
            key="failure_impact_score"
        )

    st.markdown("### Operational Data")
    col5, col6, col7, col8 = st.columns(4, gap="small")

    with col5:
        operating_hours = st.number_input(
            "Operating Hours",
            min_value=0,
            value=st.session_state.get("operating_hours", 0),
            step=100,
            key="operating_hours"
        )

    with col6:
        failure_history_count = st.number_input(
            "Failure History Count",
            min_value=0,
            value=st.session_state.get("failure_history_count", 0),
            step=1,
            key="failure_history_count"
        )

    with col7:
        days_since_maintenance = st.number_input(
            "Days Since Maintenance",
            min_value=0,
            value=st.session_state.get("days_since_maintenance", 0),
            step=1,
            key="days_since_maintenance"
        )

    with col8:
        failure_probability = st.number_input(
            "Failure Probability",
            min_value=0.01,
            max_value=0.99,
            value=st.session_state.get("failure_probability", 0.01),
            step=0.01,
            key="failure_probability"
        )

    st.markdown("### System Parameters")
    col9, col10, col11 = st.columns(3, gap="small")

    with col9:
        environmental_stress_index = st.number_input(
            "Environmental Stress Index",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.get("environmental_stress_index", 0.1),
            step=0.1,
            key="environmental_stress_index"
        )

    with col10:
        system_importance_score = st.number_input(
            "System Importance Score",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get("system_importance_score", 0.0),
            step=0.1,
            key="system_importance_score"
        )

    with col11:
        budget_constraint_flag = st.selectbox(
            "Budget Constraint",
            ["No", "Yes"],
            index=0 if st.session_state.get("budget_constraint_flag", "No") == "No" else 1,
            key="budget_constraint_flag"
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
        predicted_rul = round(float(prediction[0]), 2)
        
        st.markdown("---")
        st.markdown("### Prediction Result")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric("Predicted RUL", f"{predicted_rul:.2f} years")
        
        with res_col2:
            if predicted_rul < 3:    
             risk_level = "🔴 High"
            elif predicted_rul < 7:
                risk_level = "🟡 Medium"
            else:
                risk_level = "🟢 Low"
            st.metric("Risk Level", risk_level)
        
        with res_col3:
            priority = "Urgent" if predicted_rul < 3 else ("Moderate" if predicted_rul < 7 else "Low")
            st.metric("Priority", priority)

            # =====================================================
            # SAVE PREDICTION TO DATABASE
            # =====================================================

            cursor.execute("""

            INSERT INTO prediction_history (

                asset_type,

                condition_score,

                total_maintenance_cost,

                failure_impact_score,

                operating_hours,

                failure_history_count,

                days_since_maintenance,

                failure_probability,

                environmental_stress_index,

                system_importance_score,

                budget_constraint_flag,

                predicted_rul,

                risk_level

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """, (

                asset_type,

                condition_score,

                total_maintenance_cost,

                failure_impact_score,

                operating_hours,

                failure_history_count,

                days_since_maintenance,

                failure_probability,

                environmental_stress_index,

                system_importance_score,

                1 if budget_constraint_flag == "Yes" else 0,

                predicted_rul,

                risk_level
            ))

            conn.commit()
        
        with st.expander("📊 View Input Data"):
            st.dataframe(input_data, use_container_width=True)

elif nav_option == "Prediction History":

    st.title("Prediction History")

    def clear_history():
        cursor.execute("DELETE FROM prediction_history")
        conn.commit()
        st.session_state["history_cleared"] = True

    st.button(
        "🗑️ Clear History",
        use_container_width=True,
        on_click=clear_history,
        key="clear_history_btn"
    )

    history = pd.read_sql_query(

        "SELECT * FROM prediction_history ORDER BY id DESC",

        conn
    )

    if st.session_state.get("history_cleared"):
        st.success("Prediction history cleared.")
        st.session_state["history_cleared"] = False

    st.dataframe(

        history,

        use_container_width=True
    )

elif nav_option == "Batch Analysis":
    st.title("Batch Analysis")
    st.markdown("Upload a CSV file to predict RUL for multiple assets at once.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.markdown("### Preview")
        st.dataframe(df, use_container_width=True)
        
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