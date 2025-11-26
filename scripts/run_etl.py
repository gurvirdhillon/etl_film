import os
import sys
from config.env_config import setup_env

def main():
    if len(sys.argv) < 2:
        print("Usage: run_etl <env>")
        return
    
    env = sys.argv[1]
    print(f"Running ETL for environment: {env}")

    if env == "dev":
        # Call the ETL for dev environment
        print("Running ETL in development mode...")
        # your ETL logic here
    elif env == "test":
        print("Running ETL in production mode...")
        # prod ETL logic here
    else:
        print(f"Unknown environment: {env}")
