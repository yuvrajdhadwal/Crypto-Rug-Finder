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

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)
scaler = joblib.load(SCALER_PATH)

# === API URLs ===
ARBITRUM_SUBGRAPH_URL = "https://gateway-arbitrum.network.thegraph.com/api/48f7042b8531bbba9a96514ad4e8c7e8/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B"
ETHPLORER_API_URL = "https://api.ethplorer.io/getTopTokenHolders"
ETHPLORER_API_KEY = "EK-fewp2-ycMSQm7-3Qj3b"

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
def process_data(token_address):
    pool_data = get_pool_data(token_address)
    swap_data = get_swap_data(token_address)
    mint_data, burn_data = get_mint_burn_data(token_address)
    holders = get_top_token_holders(token_address)

    df_pools = pd.DataFrame(pool_data)
    df_swaps = pd.DataFrame(swap_data)
    df_mints = pd.DataFrame(mint_data)
    df_burns = pd.DataFrame(burn_data)

    features = {}

    # Compute Metrics
    features["mean_volumeusd"] = df_pools["volumeUSD"].astype(float).mean() if not df_pools.empty else np.nan
    features["variance_volumeusd"] = df_pools["volumeUSD"].astype(float).var() if not df_pools.empty else np.nan
    features["mean_feesusd"] = df_pools["feesUSD"].astype(float).mean() if not df_pools.empty else np.nan
    features["variance_feesusd"] = df_pools["feesUSD"].astype(float).var() if not df_pools.empty else np.nan

    features["mean_tick"] = df_swaps["tick"].astype(float).mean() if not df_swaps.empty else np.nan
    features["variance_tick"] = df_swaps["tick"].astype(float).var() if not df_swaps.empty else np.nan
    features["mean_otherTokenprice"] = df_pools["token0Price"].astype(float).mean() if not df_pools.empty else np.nan
    features["variance_otherTokenprice"] = df_pools["token0Price"].astype(float).var() if not df_pools.empty else np.nan

    features["mean_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).mean() if not df_pools.empty else np.nan
    features["variance_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).var() if not df_pools.empty else np.nan

    features["mean_txcount"] = df_pools["txCount"].astype(float).mean() if not df_pools.empty else np.nan
    features["variance_txcount"] = df_pools["txCount"].astype(float).var() if not df_pools.empty else np.nan

    features["mean_volumeotherToken"] = df_swaps["amountUSD"].astype(float).mean() if not df_swaps.empty else np.nan
    features["variance_volumeotherToken"] = df_swaps["amountUSD"].astype(float).var() if not df_swaps.empty else np.nan

    features["mean_tickupper_x"] = df_mints["tickUpper"].astype(float).mean() if not df_mints.empty else np.nan
    features["variance_tickupper_x"] = df_mints["tickUpper"].astype(float).var() if not df_mints.empty else np.nan

    features["mean_tickupper_y"] = df_burns["tickUpper"].astype(float).mean() if not df_burns.empty else np.nan
    features["variance_tickupper_y"] = df_burns["tickUpper"].astype(float).var() if not df_burns.empty else np.nan

    # Ownership Distribution
    for i, holder in enumerate(holders[:10]):
        features[f"top_owner_{i+1}_distribution"] = holder["share"]

    return features

# === Function to Make a Prediction ===
def predict_rugpull(token_address):
    features = process_data(token_address)

    # Convert to DataFrame and align with model features
    df_features = pd.DataFrame([features])
    df_features = df_features.fillna(0)  # Handle missing values

    # Preprocess features
    features_imputed = imputer.transform(df_features)
    features_scaled = scaler.transform(features_imputed)

    # Run XGBoost prediction
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {"prediction": int(prediction), "probability": float(probability)}

