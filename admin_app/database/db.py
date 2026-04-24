import pyodbc
import streamlit as st

def get_conn():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={st.secrets['database']['server']};"
        f"DATABASE={st.secrets['database']['database']};"
        "Trusted_Connection=yes;",
        timeout=5
    )
