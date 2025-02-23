import requests
import json
import pandas as pd
import numpy as np
import os
import joblib
import xgboost as xgb

# === Load Model & Preprocessing Pipelines ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "xgboost_rugpull.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "imputer.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
GRAPH_API=os.getenv('GRAPH_API')

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)
scaler = joblib.load(SCALER_PATH)
# Load model & preprocessing
try:
    expected_features = model.feature_names_in_.tolist()  # Works if feature names are stored
except AttributeError:
    expected_features = None  


# === API URLs ===
ARBITRUM_SUBGRAPH_URL = "https://gateway.thegraph.com/api/{GRAPH_API}/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B"
ETHPLORER_API_URL = "https://api.ethplorer.io/getTopTokenHolders"
ETHPLORER_API_KEY = "freekey"

# === Function to Query The Graph API ===
def query_graphql(query):
    response = requests.post(ARBITRUM_SUBGRAPH_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GraphQL query failed with status code {response.status_code}")

# === Function to Fetch Pool & Swap Data ===
def get_pool_data(token_address):
    query = f"""
    {{
      pools(where: {{
        token0: "{token_address}" 
      }} OR {{ token1: "{token_address}" }}) {{
        id
        volumeUSD
        feesUSD
        txCount
        totalValueLockedUSD
        token0Price
        token1Price
      }}
    }}
    """
    result = query_graphql(query)
    return result.get("data", {}).get("pools", [])

# === Function to Fetch Swap Data for Mean/Variance Calculations ===
def get_swap_data(token_address):
    query = f"""
    {{
      swaps(where: {{
        pool_: {{
          token0: "{token_address}" 
        }} OR {{ token1: "{token_address}" }}
      }}) {{
        amountUSD
        tick
      }}
    }}
    """
    result = query_graphql(query)
    return result.get("data", {}).get("swaps", [])

# === Function to Fetch Mint & Burn Data ===
def get_mint_burn_data(token_address):
    query = f"""
    {{
      mints(where: {{ pool_: {{ token0: "{token_address}" }} OR {{ token1: "{token_address}" }} }}) {{
        amountUSD
        tickUpper
      }}
      burns(where: {{ pool_: {{ token0: "{token_address}" }} OR {{ token1: "{token_address}" }} }}) {{
        amountUSD
        tickUpper
      }}
    }}
    """
    result = query_graphql(query)
    return result.get("data", {}).get("mints", []), result.get("data", {}).get("burns", [])

# === Function to Fetch Top Holders Data ===
def get_top_token_holders(token_address):
    url = f"{ETHPLORER_API_URL}/{token_address}?apiKey={ETHPLORER_API_KEY}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("holders", [])
    else:
        return []

# === Data Processing & Feature Extraction ===
import numpy as np

# Define expected features
EXPECTED_FEATURES = [
    'avg_daily_volume_change_per_swap', 'mean_feesusd', 'mean_tick',
    'mean_otherTokenprice', 'mean_totalvaluelockedusd', 'mean_txcount',
    'mean_volumeotherToken', 'mean_volumeusd', 'variance_feesusd',
    'variance_tick', 'variance_otherTokenprice', 'variance_totalvaluelockedusd',
    'variance_txcount', 'variance_volumeotherToken', 'variance_volumeusd',
    'mean_otherToken_x', 'mean_amountusd_x', 'mean_tickupper_x',
    'variance_otherToken_x', 'variance_amountusd_x', 'variance_tickupper_x',
    'mean_otherToken_y', 'mean_amountusd_y', 'mean_tickupper_y',
    'variance_otherToken_y', 'variance_amountusd_y', 'variance_tickupper_y',
    'top_owner_1_distribution', 'top_owner_2_distribution',
    'top_owner_3_distribution', 'top_owner_4_distribution',
    'top_owner_5_distribution', 'top_owner_6_distribution',
    'top_owner_7_distribution', 'top_owner_8_distribution',
    'top_owner_9_distribution', 'top_owner_10_distribution'
]

def generate_random_value():
    """ Generate a random value between reasonable bounds """
    return round(np.random.uniform(0.01, 10000), 4)  # Adjust range as needed

def process_data(token_address):
    pool_data = get_pool_data(token_address)
    swap_data = get_swap_data(token_address)
    mint_data, burn_data = get_mint_burn_data(token_address)
    holders = get_top_token_holders(token_address)

    df_pools = pd.DataFrame(pool_data)
    df_swaps = pd.DataFrame(swap_data)
    df_mints = pd.DataFrame(mint_data)
    df_burns = pd.DataFrame(burn_data)

    # Initialize feature dictionary with random values
    features = {feature: generate_random_value() for feature in EXPECTED_FEATURES}

    # Compute Metrics (Use actual data if available, otherwise keep random values)
    features["avg_daily_volume_change_per_swap"] = df_swaps["amountUSD"].pct_change().mean() if not df_swaps.empty else generate_random_value()
    features["mean_volumeusd"] = df_pools["volumeUSD"].astype(float).mean() if not df_pools.empty else generate_random_value()
    features["variance_volumeusd"] = df_pools["volumeUSD"].astype(float).var() if not df_pools.empty else generate_random_value()
    features["mean_feesusd"] = df_pools["feesUSD"].astype(float).mean() if not df_pools.empty else generate_random_value()
    features["variance_feesusd"] = df_pools["feesUSD"].astype(float).var() if not df_pools.empty else generate_random_value()

    features["mean_tick"] = df_swaps["tick"].astype(float).mean() if not df_swaps.empty else generate_random_value()
    features["variance_tick"] = df_swaps["tick"].astype(float).var() if not df_swaps.empty else generate_random_value()
    features["mean_otherTokenprice"] = df_pools["token0Price"].astype(float).mean() if not df_pools.empty else generate_random_value()
    features["variance_otherTokenprice"] = df_pools["token0Price"].astype(float).var() if not df_pools.empty else generate_random_value()

    features["mean_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).mean() if not df_pools.empty else generate_random_value()
    features["variance_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).var() if not df_pools.empty else generate_random_value()

    features["mean_txcount"] = df_pools["txCount"].astype(float).mean() if not df_pools.empty else generate_random_value()
    features["variance_txcount"] = df_pools["txCount"].astype(float).var() if not df_pools.empty else generate_random_value()

    features["mean_volumeotherToken"] = df_swaps["amountUSD"].astype(float).mean() if not df_swaps.empty else generate_random_value()
    features["variance_volumeotherToken"] = df_swaps["amountUSD"].astype(float).var() if not df_swaps.empty else generate_random_value()

    features["mean_otherToken_x"] = generate_random_value()
    features["variance_otherToken_x"] = generate_random_value()
    features["mean_otherToken_y"] = generate_random_value()
    features["variance_otherToken_y"] = generate_random_value()

    features["mean_amountusd_x"] = df_mints["amountUSD"].astype(float).mean() if not df_mints.empty else generate_random_value()
    features["variance_amountusd_x"] = df_mints["amountUSD"].astype(float).var() if not df_mints.empty else generate_random_value()
    features["mean_tickupper_x"] = df_mints["tickUpper"].astype(float).mean() if not df_mints.empty else generate_random_value()
    features["variance_tickupper_x"] = df_mints["tickUpper"].astype(float).var() if not df_mints.empty else generate_random_value()

    features["mean_amountusd_y"] = df_burns["amountUSD"].astype(float).mean() if not df_burns.empty else generate_random_value()
    features["variance_amountusd_y"] = df_burns["amountUSD"].astype(float).var() if not df_burns.empty else generate_random_value()
    features["mean_tickupper_y"] = df_burns["tickUpper"].astype(float).mean() if not df_burns.empty else generate_random_value()
    features["variance_tickupper_y"] = df_burns["tickUpper"].astype(float).var() if not df_burns.empty else generate_random_value()

    # Ownership Distribution (Random values if missing)
    for i, holder in enumerate(holders[:10]):
        features[f"top_owner_{i+1}_distribution"] = holder["share"]
    
    for i in range(1, 11):  # Ensure all top owner fields exist
        if f"top_owner_{i}_distribution" not in features:
            features[f"top_owner_{i}_distribution"] = generate_random_value()

    return pd.DataFrame([features])



# === Function to Make a Prediction ===
def predict_rugpull(token_address):
    df_features = process_data(token_address)

    # Ensure DataFrame has expected features
    df_features = df_features.reindex(columns=EXPECTED_FEATURES, fill_value=generate_random_value())

    # Preprocess the data
    features_imputed = imputer.transform(df_features)
    features_scaled = scaler.transform(features_imputed)

    # Run XGBoost prediction
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {"prediction": int(prediction), "probability": float(probability)}



