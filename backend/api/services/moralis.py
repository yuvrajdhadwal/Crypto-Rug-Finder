# moralis.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # This must be called BEFORE os.getenv
api_key = os.environ["MORALIS"]
def get_on_chain_info(token_address: str):
    """
    Calls Moralis to get token pairs info on Solana.
    e.g. network = 'mainnet', address = 'SRMuApVNdxX...'
    """
    url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address}/pairs?chain=eth"

    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
