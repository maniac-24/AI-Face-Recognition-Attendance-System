import streamlit as st


def metric_card(title, value, icon="📊", color="#1f77b4"):
    st.markdown(
        f"""
        <div style="
            background-color: {color}20;
            padding: 16px;
            border-radius: 12px;
            border-left: 5px solid {color};
            margin-bottom: 10px;
        ">
            <div style="font-size: 14px; color: gray;">
                {icon} {title}
            </div>
            <div style="font-size: 24px; font-weight: bold;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_row(metrics):
    """
    metrics = [
        {"title": "Total Users", "value": 10, "icon": "👥", "color": "#4CAF50"},
        {"title": "Present Today", "value": 8, "icon": "✅", "color": "#2196F3"},
    ]
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            metric_card(
                metric.get("title"),
                metric.get("value"),
                metric.get("icon", "📊"),
                metric.get("color", "#1f77b4")
            )