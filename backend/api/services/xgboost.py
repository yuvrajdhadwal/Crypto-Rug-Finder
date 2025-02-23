import requests
import json
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb

# === Constants ===
UNISWAP_API_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
ETHPLORER_API_URL = "https://api.ethplorer.io/getTopTokenHolders"
ETHPLORER_API_KEY = "EK-fewp2-ycMSQm7-3Qj3b"
MODEL_PATH = "xgboost_model.pkl"  # Update this with your actual .pkl file path

# === Function to Query Uniswap's Subgraph ===
def query_uniswap(query):
    response = requests.post(UNISWAP_API_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GraphQL query failed with status code {response.status_code}")

# === Function to Fetch Pool Data for a Given Token ===
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
      }}
    }}
    """
    result = query_uniswap(query)
    return result.get("data", {}).get("pools", [])

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
    result = query_uniswap(query)
    return result.get("data", {}).get("mints", []), result.get("data", {}).get("burns", [])

# === Function to Fetch Top Holders Data ===
def get_top_token_holders(token_address):
    url = f"{ETHPLORER_API_URL}/{token_address}?apiKey={ETHPLORER_API_KEY}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("holders", [])
    else:
        return []

# === Data Processing ===
def process_data(token_address):
    pool_data = get_pool_data(token_address)
    mint_data, burn_data = get_mint_burn_data(token_address)
    holders = get_top_token_holders(token_address)

    df_pools = pd.DataFrame(pool_data)
    df_mints = pd.DataFrame(mint_data)
    df_burns = pd.DataFrame(burn_data)

    metrics = {}

    # Compute statistical metrics
    metrics["mean_volumeusd"] = df_pools["volumeUSD"].astype(float).mean() if not df_pools.empty else np.nan
    metrics["variance_volumeusd"] = df_pools["volumeUSD"].astype(float).var() if not df_pools.empty else np.nan
    metrics["mean_feesusd"] = df_pools["feesUSD"].astype(float).mean() if not df_pools.empty else np.nan
    metrics["variance_feesusd"] = df_pools["feesUSD"].astype(float).var() if not df_pools.empty else np.nan
    metrics["mean_txcount"] = df_pools["txCount"].astype(float).mean() if not df_pools.empty else np.nan
    metrics["variance_txcount"] = df_pools["txCount"].astype(float).var() if not df_pools.empty else np.nan
    metrics["mean_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).mean() if not df_pools.empty else np.nan
    metrics["variance_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).var() if not df_pools.empty else np.nan

    metrics["mean_tickupper_x"] = df_mints["tickUpper"].astype(float).mean() if not df_mints.empty else np.nan
    metrics["variance_tickupper_x"] = df_mints["tickUpper"].astype(float).var() if not df_mints.empty else np.nan
    metrics["mean_tickupper_y"] = df_burns["tickUpper"].astype(float).mean() if not df_burns.empty else np.nan
    metrics["variance_tickupper_y"] = df_burns["tickUpper"].astype(float).var() if not df_burns.empty else np.nan

    # Ownership distribution
    for i, holder in enumerate(holders[:10]):
        metrics[f"top_owner_{i+1}_distribution"] = holder["share"]

    return pd.DataFrame([metrics])

# === Function to Load the XGBoost Model ===
def load_xgboost_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

# === Function to Make a Prediction ===
def predict_price(data):
    model = load_xgboost_model()
    
    # Ensure feature alignment
    model_features = model.feature_names  # Assuming the model was trained with feature names
    data = data[model_features].fillna(0)  # Fill missing values with 0
    
    prediction = model.predict(xgb.DMatrix(data))
    return prediction[0]
