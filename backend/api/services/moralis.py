import requests
from moralis import sol_api

api_key = ""

params = {
  "network": "mainnet",
  "address": "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt"
}

result = sol_api.token.get_token_price(
  api_key=api_key,
  params=params,
)


def get_on_chain_info(chain, address):

    url = "https://deep-index.moralis.io/api/v2.2/tokens/search?query=pepe&chains=eth"

    headers = {
    "Accept": "application/json",
    "X-API-Key": ""
    }

    response = requests.request("GET", url, headers=headers)
