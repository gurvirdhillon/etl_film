import psycopg2
from '../src/extract/extract.py' import table_to_dataframe

def test_db_connection():
    try:
        conn = psycopg2.connect(**table_to_dataframe)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM actor;")  # test table in Pagila
        result = cursor.fetchone()

        assert result is not None
        print(f"Connection successful! Actor rows: {result[0]}")

        cursor.close()
        conn.close()
        
    except Exception as e:
        assert False, f"Database connection failed: {e}"
