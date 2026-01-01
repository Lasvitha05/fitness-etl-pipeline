
#  Strava to Snowflake: End-to-End ETL Pipeline
##  Project Overview
This project is an automated ETL (Extract, Transform, Load) pipeline that extracts fitness activity data from the Strava API, transforms and enriches it with mock marketing data (simulating a MarTech environment), loads it into a Data Lake (AWS S3), and finally orchestrates ingestion into a Data Warehouse (Snowflake).
##  Architecture
Strava API (Source) $\rightarrow$ Python (Extraction & Transformation) $\rightarrow$ AWS S3 (Raw Layer) $\rightarrow$ Snowflake (Warehousing)
##  Tech Stack
#### Language: Python 3.9+
#### Libraries: pandas, requests, boto3 (AWS SDK), snowflake-connector-python
#### Cloud Storage: AWS S3
#### Data Warehouse: Snowflake
#### Security: OAuth 2.0 (Strava), IAM Roles (AWS), Storage Integrations (Snowflake)
##  Key Features
### OAuth 2.0 Handshake: 
Automates authentication with Strava using Refresh Tokens to allow continuous data extraction without manual login.
### MarTech Simulation: 
"Enriches" single-user data into a 50,000-row dataset, adding marketing dimensions like subscription_tier, acquisition_channel, and churn_risk to simulate a real-world business scenario.
### Cloud Orchestration: 
A single Python script handles the logic to upload to S3 and immediately trigger the Snowflake COPY INTO command.
### Security Best Practices: 
Utilizes .env files for credential management and AWS IAM Roles for secure S3-to-Snowflake communication.
##  Data Flow
#### Extract: 
Python hits Strava API endpoints to fetch activity data.
#### Transform:
Calculates 'Workout Intensity' based on speed.Assigns mock 'Churn Risk' based on activity frequency and subscription status.Generates 50k rows of mock data based on the seed data.
### Load (Stage 1): 
Uploads the enriched JSON data to an AWS S3 Bucket (fitness-martech-data).
### Load (Stage 2): 
Connects to Snowflake, utilizing an External Stage and File Format to ingest data into the FITNESS_MARTECH_DB.
##  Setup & Usage
#### Clone the repo:
Bashgit clone https://github.com/YOUR_USERNAME/fitness-etl-pipeline.git
#### Install dependencies:
Bashpip install -r requirements.txt
#### Configure Environment:
Create a .env file with your credentials (see .env.example).
#### Run the Pipeline:
Bashpython src/main_pipeline.py
##  Analytics Showcase

### Business Question: 
"Which marketing channel has the poorest user retention?"

**SQL Logic for Snowflake:**
```sql
SELECT 
    raw_data:acquisition_channel::STRING AS acquisition_channel,
    COUNT(*) AS total_users,
    ROUND((SUM(CASE WHEN raw_data:churn_risk::STRING = 'High' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS churn_rate_pct
FROM FITNESS_MARTECH_DB.RAW_DATA.STRAVA_DATA_RAW
GROUP BY 1 ORDER BY 3 DESC;
