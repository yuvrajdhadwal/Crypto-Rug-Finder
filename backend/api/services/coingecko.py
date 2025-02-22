import requests

def fetch_market_data(token_ids, vs_currency="usd"):
    """
    Fetch market data for the given tokens from CoinGecko.
    
    :param token_ids: List of CoinGecko token IDs (e.g., ["ethereum", "uniswap", "bitcoin"])
    :param vs_currency: The target currency (default: "usd")
    :return: List of market data dictionaries
    """
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&x_cg_demo_api_key=?"
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(token_ids),
        "order": "market_cap_desc",
        "per_page": len(token_ids),
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code, response.text)
        return []

if __name__ == "__main__":
    tokens = ["ethereum", "uniswap", "bitcoin"]
    market_data = fetch_market_data(tokens)
    for token in market_data:
        print(f"{token['name']} ({token['id']}):")
        print(f"  Current Price: ${token['current_price']}")
        print(f"  Total Volume: ${token['total_volume']}")
        print(f"  Market Cap: ${token['market_cap']}\n")
