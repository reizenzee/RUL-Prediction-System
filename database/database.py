import sqlite3

# =====================================================
# CONNECT SQLITE DATABASE
# =====================================================

conn = sqlite3.connect(

    "database/rul_prediction.db",

    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS prediction_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_type TEXT,

    condition_score REAL,

    total_maintenance_cost REAL,

    failure_impact_score REAL,

    operating_hours REAL,

    failure_history_count INTEGER,

    days_since_maintenance INTEGER,

    failure_probability REAL,

    environmental_stress_index REAL,

    system_importance_score REAL,

    budget_constraint_flag INTEGER,

    predicted_rul REAL,

    risk_level TEXT,

    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

conn.commit()