import pyodbc


def get_conn():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"   # change if needed
            "DATABASE=attendance_db;"
            "Trusted_Connection=yes;"
        )
        return conn

    except Exception as e:
        print(f"Database connection error: {e}")
        return None