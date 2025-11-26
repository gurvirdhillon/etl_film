import os
import sys
from config.env_config import setup_env
from src.extract.extract import table_to_csv
from src.transform.transform import run_cleaners
def main():
    if len(sys.argv) < 2:
        print("Usage: run_etl <env>")
        return
    
    env = sys.argv[1]
    print(f"Running ETL for environment: {env}")

    if env == "dev":
        print("Running ETL in development mode...")
        table_to_csv()
        run_cleaners()
        



    elif env == "test":
        print("Running ETL in production mode...")
        # prod ETL logic here
    else:
        print(f"Unknown environment: {env}")
