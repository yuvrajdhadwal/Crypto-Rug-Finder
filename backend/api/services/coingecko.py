import requests
import os

# CoinGecko API Base URL
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Function to fetch all tokens and their details from CoinGecko
def fetch_all_tokens():
    url = f"{COINGECKO_BASE_URL}/coins/list"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # List of all tokens
    else:
        print(f"Error fetching token list: {response.status_code}")
        return []

# Function to find contract address given a token symbol (e.g., "TRUMP")
def get_contract_address(token_symbol):
    tokens = fetch_all_tokens()
    
    for token in tokens:
        if token["symbol"].lower() == token_symbol.lower():
            return token["id"]  # Return CoinGecko's ID for this token
    
    return None  # If token is not found

# Function to fetch market data for a given token ID
def fetch_market_data(token_id, vs_currency="usd"):
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "ids": token_id,
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": "false",
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()[0]  # Return first result
    else:
        print(f"Error fetching market data: {response.status_code}")
        return None

# Function to get token details (Contract Address + Market Data)
def get_token_info(symbol):
    token_id = get_contract_address(symbol)
    
    if not token_id:
        return {"error": f"Token symbol '{symbol}' not found on CoinGecko."}
    
    market_data = fetch_market_data(token_id)
    
    if not market_data:
        return {"error": f"Market data for '{symbol}' could not be retrieved."}
    
    return {
        "name": market_data["name"],
        "symbol": symbol.upper(),
        "contract_address": token_id,  # CoinGecko ID acts as a reference
        "current_price": market_data["current_price"],
        "total_volume": market_data["total_volume"],
        "market_cap": market_data["market_cap"],
    }

