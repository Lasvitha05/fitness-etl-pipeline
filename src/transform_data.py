import json
import random
import os
from datetime import datetime, timedelta

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'strava_raw_data.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'enriched_fitness_market_data.json')
NUM_ROWS = 50000 

# Mock Data Constants
SUBSCRIPTION_TIERS = ['Free', 'Premium', 'Pro_Annual']
ACQUISITION_CHANNELS = ['Instagram_Ad', 'Referral', 'Organic_Search', 'Influencer_Campaign', 'Email_Promo']
DEVICES = ['Garmin', 'Apple Watch', 'Fitbit', 'Strava App', 'Peloton']

def load_real_data():
    try:
        with open(INPUT_FILE, 'r') as f:
            data = json.load(f)
            return data[0] if data else None
    except FileNotFoundError:
        print(f" Could not find {INPUT_FILE}. Run extract_strava.py first.")
        return None

def generate_mock_dataset(template):
    mock_data = []
    for i in range(NUM_ROWS):
        row = template.copy()
        # Randomize Data
        dist_variance = random.uniform(0.5, 1.5) 
        row['distance'] = round(row['distance'] * dist_variance, 2)
        row['moving_time'] = int(row['moving_time'] * dist_variance)
        row['user_id'] = random.randint(1000, 6000)
        
        # MarTech Enrichment
        row['subscription_status'] = random.choices(SUBSCRIPTION_TIERS, weights=[60, 30, 10])[0]
        row['acquisition_channel'] = random.choice(ACQUISITION_CHANNELS)
        row['device_type'] = random.choice(DEVICES)
        
        # Logic for Churn Risk
        speed = row['distance'] / row['moving_time'] if row['moving_time'] > 0 else 0
        intensity = 'High' if speed > 3.5 else 'Medium' if speed > 2.5 else 'Low'
        row['intensity_label'] = intensity
        
        if row['subscription_status'] == 'Free' and intensity == 'Low':
            row['churn_risk'] = 'High'
        else:
            row['churn_risk'] = 'Low'

        mock_data.append(row)
    return mock_data

if __name__ == "__main__":
    template = load_real_data()
    if template:
        print(f"Generating {NUM_ROWS} rows...")
        enriched_data = generate_mock_dataset(template)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(enriched_data, f, indent=4)
        print(f" Enriched data saved to {OUTPUT_FILE}")