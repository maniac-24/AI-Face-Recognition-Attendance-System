import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_panel(df):
    st.subheader("🚨 Alerts & Admin Panel")

    if df.empty:
        st.warning("No data")
        return

    threshold = st.slider("Minimum attendance days", 1, 30, 5)

    df_copy = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df_copy['date']):
        df_copy['date'] = pd.to_datetime(df_copy['date'])

    df_copy["month"] = df_copy["date"].dt.month
    current_month = datetime.now().month

    monthly = df_copy[df_copy["month"] == current_month]
    counts = monthly.groupby("name").size()

    low = counts[counts < threshold]

    st.write("⚠️ Low Attendance Users")

    if low.empty:
        st.success("✅ No low attendance issues")
    else:
        for name, count in low.items():
            st.warning(f"{name} → {count} days")