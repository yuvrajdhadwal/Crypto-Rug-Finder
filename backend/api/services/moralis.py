# moralis.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # This must be called BEFORE os.getenv
api_key = os.getenv("MORALIS_API")
def get_on_chain_info(network: str, address: str):
    """
    Calls Moralis to get token pairs info on Solana.
    e.g. network = 'mainnet', address = 'SRMuApVNdxX...'
    """
    url = f"https://solana-gateway.moralis.io/token/{network}/{address}/pairs"

    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
