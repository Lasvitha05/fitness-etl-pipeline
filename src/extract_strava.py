import requests
import json
import os
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'strava_raw_data.json')

def get_access_token():
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token',
        'f': 'json'
    }
    
    response = requests.post(url, data=payload, verify=False)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(" Error refreshing token:", response.json())
        exit()

def fetch_data(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f"Bearer {access_token}"}
    params = {'per_page': 50, 'page': 1}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    token = get_access_token()
    print("Fetching activities...")
    data = fetch_data(token)
    
    if isinstance(data, list) and len(data) > 0:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f" Success! Data saved to {OUTPUT_FILE}")
    else:
        print(" No data found or error occurred.")