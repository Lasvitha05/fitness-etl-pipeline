import boto3
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION FROM .ENV ---
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_FILENAME = os.path.join(BASE_DIR, 'data', 'enriched_fitness_market_data.json')
S3_FILENAME = "raw_layer/strava_marketing_v1.json"

def upload_to_s3(s3_client):
    if not os.path.exists(LOCAL_FILENAME):
        print(f" File not found: {LOCAL_FILENAME}")
        return False
    try:
        print(f" Uploading to S3 bucket: {BUCKET_NAME}...")
        s3_client.upload_file(LOCAL_FILENAME, BUCKET_NAME, S3_FILENAME)
        print(" Upload Successful")
        return True
    except Exception as e:
        print(f" Upload Failed: {e}")
        return False

def trigger_snowflake():
    print(" Connecting to Snowflake...")
    try:
        ctx = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DB,
            schema=SNOWFLAKE_SCHEMA
        )
        cs = ctx.cursor()
        
        # Ingestion Query
        copy_sql = f"""
        COPY INTO strava_data_raw (raw_data)
        FROM (SELECT $1 FROM @my_s3_stage)
        PATTERN = '.*.json'
        ON_ERROR = 'CONTINUE';
        """
        cs.execute(copy_sql)
        
        # Verify
        cs.execute("SELECT COUNT(*) FROM strava_data_raw")
        count = cs.fetchone()[0]
        print(f" Snowflake Ingestion Complete! Total Rows: {count}")
    except Exception as e:
        print(f" Snowflake Error: {e}")
    finally:
        if 'ctx' in locals(): ctx.close()

if __name__ == "__main__":
    s3 = boto3.client(
        's3', 
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    
    if upload_to_s3(s3):
        trigger_snowflake()