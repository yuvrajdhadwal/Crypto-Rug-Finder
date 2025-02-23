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
GRAPH_API = os.getenv("GRAPH_API")

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)
scaler = joblib.load(SCALER_PATH)
try:
    expected_features = model.feature_names_in_.tolist()  # Use feature names stored in the model, if available
except AttributeError:
    expected_features = [
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

# === API URLs ===
ARBITRUM_SUBGRAPH_URL = "https://gateway.thegraph.com/api/4e1f3dae578c715c6ea8b3054a74bf86/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B"
ETHPLORER_API_URL = "https://api.ethplorer.io/getTopTokenHolders"
ETHPLORER_API_KEY = "freekey"

# === GraphQL Query Function ===
def query_graphql(query):
    headers = {"Content-Type": "application/json"}
    # Clean the query string
    cleaned_query = " ".join(query.split())
    payload = {"query": cleaned_query}

    print(f"🚀 Sending GraphQL Request to: {ARBITRUM_SUBGRAPH_URL}")
    print(f"📜 Query: {json.dumps(payload, indent=2)}")
    
    response = requests.post(ARBITRUM_SUBGRAPH_URL, headers=headers, json=payload)
    print(f"🔍 Status Code: {response.status_code}")
    print(f"📜 Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            return data
        else:
            print("⚠️ Warning: API returned no 'data' key. Response:", data)
            return {}
    else:
        print(f"❌ GraphQL query failed! Status: {response.status_code}, Response: {response.text}")
        return {}

# === Helper Function: Get Pools Involving the Coin ===
def get_pools_by_coin(token_address):
    pools = {}
    # Query pools where token0 equals token_address
    last_id = ""
    while True:
        query = f"""
        {{
          pools(first: 1000, orderBy: id, orderDirection: asc, where: {{
            id_gt: "{last_id}",
            token0: "{token_address}"
          }}) {{
            id
            token0 {{ id }}
            token1 {{ id }}
          }}
        }}
        """
        result = query_graphql(query)
        data = result.get("data", {}).get("pools", [])
        if not data:
            break
        for pool in data:
            pools[pool["id"]] = pool
        last_id = data[-1]["id"]
    
    # Query pools where token1 equals token_address
    last_id = ""
    while True:
        query = f"""
        {{
          pools(first: 1000, orderBy: id, orderDirection: asc, where: {{
            id_gt: "{last_id}",
            token1: "{token_address}"
          }}) {{
            id
            token0 {{ id }}
            token1 {{ id }}
          }}
        }}
        """
        result = query_graphql(query)
        data = result.get("data", {}).get("pools", [])
        if not data:
            break
        for pool in data:
            pools[pool["id"]] = pool
        last_id = data[-1]["id"]
    
    return list(pools.values())

# === Function to Fetch Pool Data for the Coin ===
def get_pool_data(token_address):
    pools = get_pools_by_coin(token_address)
    pool_ids = [pool["id"] for pool in pools]
    if not pool_ids:
        return []
    # Format the pool IDs as a GraphQL list
    pool_ids_str = "[" + ", ".join(f'"{pid}"' for pid in pool_ids) + "]"
    query = f"""
    {{
      pools(where: {{
        id_in: {pool_ids_str}
      }}) {{
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

# === Function to Fetch Swap Data for the Coin ===
def get_swap_data(token_address):
    pools = get_pools_by_coin(token_address)
    pool_ids = [pool["id"] for pool in pools]
    if not pool_ids:
        return []
    pool_ids_str = "[" + ", ".join(f'"{pid}"' for pid in pool_ids) + "]"
    query = f"""
    {{
      swaps(where: {{
        pool_in: {pool_ids_str}
      }}) {{
        amountUSD
        tick
      }}
    }}
    """
    result = query_graphql(query)
    return result.get("data", {}).get("swaps", [])

# === Function to Fetch Mint & Burn Data for the Coin ===
def get_mint_burn_data(token_address):
    pools = get_pools_by_coin(token_address)
    pool_ids = [pool["id"] for pool in pools]
    if not pool_ids:
        return ([], [])
    pool_ids_str = "[" + ", ".join(f'"{pid}"' for pid in pool_ids) + "]"
    query = f"""
    {{
      mints(where: {{
        pool_in: {pool_ids_str}
      }}) {{
        amountUSD
        tickUpper
      }}
      burns(where: {{
        pool_in: {pool_ids_str}
      }}) {{
        amountUSD
        tickUpper
      }}
    }}
    """
    result = query_graphql(query)
    mints = result.get("data", {}).get("mints", [])
    burns = result.get("data", {}).get("burns", [])
    return mints, burns

# === Function to Fetch Top Token Holders Data ===
def get_top_token_holders(token_address):
    url = f"{ETHPLORER_API_URL}/{token_address}?apiKey={ETHPLORER_API_KEY}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("holders", []) if isinstance(data.get("holders"), list) else []
    else:
        print(f"❌ Ethplorer API failed with status code {response.status_code}")
        return []

# === Data Processing & Feature Extraction ===
def process_data(token_address):
    pool_data = get_pool_data(token_address)
    swap_data = get_swap_data(token_address)
    mint_data, burn_data = get_mint_burn_data(token_address)
    holders = get_top_token_holders(token_address)

    print(f"🚀 Pool Data: {pool_data}")
    print(f"🚀 Swap Data: {swap_data}")
    print(f"🚀 Mint Data: {mint_data}")
    print(f"🚀 Burn Data: {burn_data}")
    print(f"🚀 Holders Data: {holders}")

    pool_data = pool_data if isinstance(pool_data, list) else []
    swap_data = swap_data if isinstance(swap_data, list) else []
    mint_data = mint_data if isinstance(mint_data, list) else []
    burn_data = burn_data if isinstance(burn_data, list) else []
    holders = holders if isinstance(holders, list) else []

    df_pools = pd.DataFrame(pool_data)
    df_swaps = pd.DataFrame(swap_data)
    df_mints = pd.DataFrame(mint_data)
    df_burns = pd.DataFrame(burn_data)

    # Initialize features dictionary with zeros
    features = {feature: 0.0 for feature in expected_features}

    # Example Metrics Calculation
    if not df_swaps.empty and "amountUSD" in df_swaps.columns:
        try:
            features["avg_daily_volume_change_per_swap"] = df_swaps["amountUSD"].pct_change().mean()
        except Exception as e:
            print("Error calculating avg_daily_volume_change_per_swap:", e)

    if not df_pools.empty:
        if "volumeUSD" in df_pools.columns:
            features["mean_volumeusd"] = df_pools["volumeUSD"].astype(float).mean()
            features["variance_volumeusd"] = df_pools["volumeUSD"].astype(float).var()
        if "feesUSD" in df_pools.columns:
            features["mean_feesusd"] = df_pools["feesUSD"].astype(float).mean()
            features["variance_feesusd"] = df_pools["feesUSD"].astype(float).var()
        if "txCount" in df_pools.columns:
            features["mean_txcount"] = df_pools["txCount"].astype(float).mean()
            features["variance_txcount"] = df_pools["txCount"].astype(float).var()
        if "token0Price" in df_pools.columns and "token1Price" in df_pools.columns:
            # Assuming 'otherTokenprice' represents the price of the paired token (adjust as needed)
            features["mean_otherTokenprice"] = df_pools[["token0Price", "token1Price"]].mean().mean()
            features["variance_otherTokenprice"] = df_pools[["token0Price", "token1Price"]].var().mean()
        if "totalValueLockedUSD" in df_pools.columns:
            features["mean_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).mean()
            features["variance_totalvaluelockedusd"] = df_pools["totalValueLockedUSD"].astype(float).var()

    if holders:
        for i, holder in enumerate(holders[:10]):
            features[f"top_owner_{i+1}_distribution"] = holder.get("share", 0)

    return pd.DataFrame([features])

# === Function to Make a Prediction ===
def predict_rugpull(token_address):
    df_features = process_data(token_address)
    print("Features in df_features Before Alignment:\n", df_features.columns.tolist())
    # Ensure the DataFrame has all expected features in the correct order
    df_features = df_features.reindex(columns=expected_features, fill_value=0)
    print("Features in df_features After Alignment:\n", df_features.columns.tolist())
    df_features = df_features.astype(float)
    features_imputed = imputer.transform(df_features)
    features_scaled = scaler.transform(features_imputed)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]
    return {"prediction": int(prediction), "probability": float(probability)}
