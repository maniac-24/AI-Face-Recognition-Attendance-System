import streamlit as st
import pandas as pd
import math
from datetime import datetime
from utils.helpers import img_to_base64


def show_dashboard(df_input):
    st.markdown("## 📊 Attendance Dashboard")

    if df_input.empty:
        st.warning("No data available")
        return

    # ---------------- PREPROCESS ---------------- #
    df = df_input.copy()
    df.rename(columns={'name': 'Name', 'date': 'Date', 'status': 'Status'}, inplace=True)

    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])

    # Only approved users
    if 'status_user' in df.columns:
        df = df[df['status_user'] == 'approved']

    # ---------------- METRICS ---------------- #
    st.markdown("### 📈 Daily Overview")

    today = datetime.now().date()
    today_data = df[df['Date'].dt.date == today]

    VALID_PRESENT = ['Full Day', 'Late Full Day', 'Half Day']
    VALID_LATE = ['Late Full Day', 'Half Day']

    total_users = df['Name'].nunique()
    present_today = len(today_data[today_data['Status'].isin(VALID_PRESENT)])
    late_today = len(today_data[today_data['Status'].isin(VALID_LATE)])

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Users", total_users)
    col2.metric("✅ Present Today", present_today)
    col3.metric("⏰ Late/Half Day", late_today)

    st.markdown("---")

    # ---------------- FILTERS ---------------- #
    st.markdown("### 🔍 Filters")

    if st.button("📅 Today Only"):
        df = df[df['Date'].dt.date == today]

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        search = st.text_input("Search Name")

    with f2:
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.date_input("Date Range", [min_date, max_date])

    with f3:
        statuses = st.multiselect(
            "Status",
            sorted(df['Status'].dropna().unique()),
            default=list(df['Status'].dropna().unique())
        )

    with f4:
        users = st.multiselect(
            "Users",
            sorted(df['Name'].unique())
        )

    # ---------------- APPLY FILTERS ---------------- #
    filtered = df.copy()

    if search:
        filtered = filtered[filtered['Name'].str.contains(search, case=False)]

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        filtered = filtered[
            (filtered['Date'].dt.date >= date_range[0]) &
            (filtered['Date'].dt.date <= date_range[1])
        ]

    if statuses:
        filtered = filtered[filtered['Status'].isin(statuses)]

    if users:
        filtered = filtered[filtered['Name'].isin(users)]

    st.markdown("---")

    # ---------------- ANALYTICS ---------------- #
    with st.expander("📊 Insights"):
        colA, colB = st.columns(2)

        with colA:
            st.markdown("**Attendance %**")
            if not filtered.empty:
                total = filtered.groupby("Name").size()
                present = filtered[filtered['Status'].isin(VALID_PRESENT)].groupby("Name").size()
                pct = (present / total * 100).fillna(0).round(1).reset_index(name="Attendance %")
                pct["Attendance %"] = pct["Attendance %"].astype(str) + "%"
                st.dataframe(pct, use_container_width=True, hide_index=True)

        with colB:
            st.markdown("**Monthly Trend**")
            if not filtered.empty:
                temp = filtered.copy()
                temp["Month"] = temp["Date"].dt.strftime('%b %Y')
                chart = temp.groupby(["Month", "Status"]).size().unstack(fill_value=0)
                st.bar_chart(chart)

    # ---------------- TABLE ---------------- #
    st.markdown("### 📋 Records")

    if filtered.empty:
        st.info("No records found")
        return

    filtered = filtered.sort_values(by="Date", ascending=False)

    # Pagination
    col1, col2 = st.columns([1, 3])
    with col1:
        rows = st.selectbox("Rows", [5, 10, 20, 50], index=1)

    total_pages = math.ceil(len(filtered) / rows)
    with col2:
        page = st.number_input("Page", 1, max(1, total_pages), 1)

    start = (page - 1) * rows
    end = start + rows

    display = filtered.iloc[start:end].copy()
    display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")

    # Image column
    if "photo" in display.columns:
        display["Profile"] = display["photo"].apply(img_to_base64)
    else:
        display["Profile"] = None

    display = display.drop(columns=["photo"], errors="ignore")

    st.dataframe(
        display,
        column_config={
            "Profile": st.column_config.ImageColumn("Profile"),
        },
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Showing {start+1}–{min(end, len(filtered))} of {len(filtered)}")

    # ---------------- EXPORT ---------------- #
    st.markdown("---")

    export_df = filtered.drop(columns=["photo"], errors="ignore")
    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        file_name=f"attendance_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )