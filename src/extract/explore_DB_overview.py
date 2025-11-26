from sqlalchemy import create_engine, text
import sys

# --------------------------
# CONFIGURATION
# --------------------------
DB_USER = "de14_savy"
DB_PASS = "BF9TtHsy"
DB_HOST = "data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "pagila"
DB_SCHEMA = "main"

# Connect to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?options=-csearch_path%3D{DB_SCHEMA}"
)


def get_table_info():
    """Get overview of all tables in the database"""
    with engine.connect() as conn:
        # Get list of tables
        tables = conn.execute(
            text(f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = '{DB_SCHEMA}' AND table_type='BASE TABLE';
            """)
        ).fetchall()
        tables = [t[0] for t in tables]
        print(f"Found tables: {tables}\n")

        # Iterate over each table
        for table in tables:
            print(f"--- Table: {table} ---")

            # Get columns and types
            try:
                cols = conn.execute(text(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = '{table}';
                """)).fetchall()
                print("Columns and types:")
                for col_name, col_type in cols:
                    print(f"  {col_name}: {col_type}")
            except Exception as e:
                print(f"  Could not fetch columns for {table}: {e}")
                conn.rollback()
                continue

            # Get row count
            try:
                row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"Row count: {row_count}")
            except Exception as e:
                print(f"  Could not fetch row count for {table}: {e}")
                conn.rollback()
                row_count = "N/A"

            # Unique counts for text/varchar columns
            for col_name, col_type in cols:
                if col_type in ("character varying", "text", "varchar"):
                    try:
                        unique_count = conn.execute(
                            text(f'SELECT COUNT(DISTINCT "{col_name}") FROM {table}')
                        ).scalar()
                        print(f"  {col_name} unique values: {unique_count}")
                    except Exception as e:
                        print(f"  Skipped unique count for {col_name}: {e}")
                        conn.rollback()

            print("")  # Spacer between tables


def main():
    try:
        get_table_info()
    except Exception as e:
        print(f"Error during DB overview: {e}")


if __name__ == "__main__":
    main()
