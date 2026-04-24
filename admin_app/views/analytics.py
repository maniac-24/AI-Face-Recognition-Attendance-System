import streamlit as st
import pandas as pd

def show_analytics(df):
    st.subheader("📈 Analytics Dashboard")

    if df.empty:
        st.warning("No data available")
        return

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # -------- FILTERS -------- #
    col1, col2 = st.columns(2)

    with col1:
        year = st.selectbox(
            "Select Year",
            sorted(df["date"].dt.year.unique())
        )

    with col2:
        month = st.selectbox(
            "Select Month",
            sorted(df[df["date"].dt.year == year]["date"].dt.month.unique())
        )

    df = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]

    # -------- STATUS LOGIC -------- #
    present_status = ["Full Day", "Late Full Day", "Half Day", "Early Leave"]

    total_records = len(df)
    unique_users = df["name"].nunique()
    present_count = df[df["status"].isin(present_status)].shape[0]
    attendance_rate = (present_count / total_records * 100) if total_records else 0

    # -------- KPIs -------- #
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📄 Total Records", total_records)
    c2.metric("👤 Users", unique_users)
    c3.metric("✅ Present", present_count)
    c4.metric("📊 Attendance %", f"{attendance_rate:.2f}%")

    st.markdown("---")

    # -------- USER PERFORMANCE -------- #
    st.subheader("🏆 User Attendance (Count)")
    user_counts = df["name"].value_counts()
    st.bar_chart(user_counts)

    st.success("Top Performers")
    st.write(user_counts.head(3))

    st.error("Low Performers")
    st.write(user_counts.tail(3))

    st.markdown("---")

    # -------- DAILY TREND -------- #
    st.subheader("📅 Daily Trend")
    daily = df.groupby("date").size()
    st.line_chart(daily)

    st.markdown("---")

    # -------- STATUS DISTRIBUTION -------- #
    st.subheader("📊 Status Distribution")
    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

    st.markdown("---")

    # =========================================================
    # 🔥 ADVANCED INSIGHTS (your additions properly integrated)
    # =========================================================

    # -------- ABSENTEE LEADERBOARD -------- #
    st.subheader("❌ Absentee Leaderboard")

    absent_df = df[~df["status"].isin(present_status)]

    if not absent_df.empty:
        absent_counts = absent_df["name"].value_counts()
        st.bar_chart(absent_counts)
        st.write(absent_counts)
    else:
        st.success("No absentees 🎉")

    st.markdown("---")

    # -------- LATE ARRIVALS -------- #
    st.subheader("⏰ Late Arrivals")

    late_df = df[df["status"] == "Late Full Day"]

    if not late_df.empty:
        late_counts = late_df["name"].value_counts()
        st.bar_chart(late_counts)
        st.write(late_counts)
    else:
        st.success("No late arrivals 👍")

    st.markdown("---")

    # -------- WEEKLY TREND -------- #
    st.subheader("📆 Weekly Trend")

    df["week"] = df["date"].dt.isocalendar().week
    weekly = df.groupby("week").size()

    st.line_chart(weekly)

    st.markdown("---")

    # -------- PIVOT TABLE -------- #
    st.subheader("📌 Attendance Table")

    pivot = pd.pivot_table(
        df,
        index="name",
        columns="date",
        values="status",
        aggfunc="first"
    )

    st.dataframe(pivot, use_container_width=True)

    st.markdown("---")

    # -------- DOWNLOAD -------- #
    st.download_button(
        "⬇ Download Report",
        df.to_csv(index=False),
        file_name=f"attendance_{year}_{month}.csv",
        mime="text/csv"
    )