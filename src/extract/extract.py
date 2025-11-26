from sqlalchemy import create_engine, text
import pandas as pd
import sys


def table_to_dataframe():

    engine = create_engine("postgresql+psycopg2://de14_albe:modGdY98@data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com:5432/pagila?options=-csearch_path%3Dmain")

    tables = ("payment", "film", "app_id", "rental", "customer", "film_actor", "actor", "staff", "store", "address", "city", "country", "inventory", "language", "film_category", "category")

    with engine.connect() as conn:

        for table_name in tables:
            try:
                df = pd.read_sql(text(f"""
                                    SELECT
                                        *
                                    FROM
                                        {table_name}
                                    """), conn)
            except Exception as e:
                print(f"Extraction failed - Check list of table names :", e)
                return

            try:
                df.to_csv(f"data/output/{table_name}.csv", index=False)
            except Exception as e:
                print(f"Failed to create or update {table_name} csv at data/output. Error: {e}")


def main():

    # if len(sys.argv) < 2:
    #     print("Usage: python extract.py <table_name>")
    #     return

    # table_name = sys.argv[1]
    # columns = sys.argv[2]
    table_to_dataframe()


if __name__ == "__main__":
    main()
