# backend/api/services/honeypot.py
import requests

HONEYPOT_API_URL = "https://api.honeypot.is/v2/IsHoneypot"

def check_honeypot(token_address: str, chain: str = "eth"):
    """
    Calls the Honeypot API to check if a given token is a honeypot.
    
    :param token_address: The token contract address (e.g., 0xA0b8...)
    :param chain: The blockchain chain identifier, e.g. 'eth', 'bsc', 'polygon' if supported
    :return: Parsed JSON response from Honeypot API or an error dict
    """
    # The docs only show a cURL example, but it's typically a GET or POST with query/body parameters.
    # Example query param approach: ?chain=eth&token=0xA0b8...
    # If the doc states it's a GET with param 'token=' or a POST body, adapt accordingly.

    params = {
        "chain": chain,
        "token": token_address
    }
    
    try:
        response = requests.get(HONEYPOT_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError if not 2xx
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        # Handle HTTP errors, timeouts, etc.
        print("Honeypot API error:", e)
        return {"error": str(e)}
