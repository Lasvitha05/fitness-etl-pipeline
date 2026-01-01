import pandas as pd
import json
import os

# Define file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'enriched_fitness_market_data.json')

def analyze_churn():
    # 1. Load the Data
    print("Loading local data...")
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    # 2. Replicate the SQL Logic
    # SQL: SUM(CASE WHEN churn_risk = 'High'...)
    # Python: GroupBy + Lambda logic
    
    analysis = df.groupby('acquisition_channel').apply(
        lambda x: pd.Series({
            'Total_Users': len(x),
            'High_Risk_Users': (x['churn_risk'] == 'High').sum(),
            'Churn_Rate_Pct': round(((x['churn_risk'] == 'High').sum() / len(x)) * 100, 2)
        })
    ).reset_index()

    # 3. Sort by Churn Rate (just like the SQL 'ORDER BY 4 DESC')
    analysis = analysis.sort_values(by='Churn_Rate_Pct', ascending=False)

    # 4. Pretty Print the Results
    print("\n" + "="*50)
    print(" MOCK MARTECH ANALYSIS (Local Pandas Fallback)")
    print("="*50)
    print(analysis.to_string(index=False))
    print("="*50 + "\n")

if __name__ == "__main__":
    if os.path.exists(DATA_FILE):
        analyze_churn()
    else:
        print(" Data file not found. Run transform_data.py first.")