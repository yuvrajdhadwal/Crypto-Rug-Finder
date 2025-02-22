import requests
from moralis import sol_api

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjYxYjZmYmU5LWQ0NWItNDIzNC1hZGRmLWQwNzgyY2IxZDliNiIsIm9yZ0lkIjoiNDMyOTE1IiwidXNlcklkIjoiNDQ1MzI3IiwidHlwZUlkIjoiMTJiYjcxYzQtNzBjOC00MDI0LWE5YjItOWFiYTFkOGZjYzdiIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDAyMDU0NTQsImV4cCI6NDg5NTk2NTQ1NH0._9y_wAuVGB6kyzg9-mjIqHuiWzMrExCB41FeJ76mMZs"

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
    "X-API-Key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjYxYjZmYmU5LWQ0NWItNDIzNC1hZGRmLWQwNzgyY2IxZDliNiIsIm9yZ0lkIjoiNDMyOTE1IiwidXNlcklkIjoiNDQ1MzI3IiwidHlwZUlkIjoiMTJiYjcxYzQtNzBjOC00MDI0LWE5YjItOWFiYTFkOGZjYzdiIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDAyMDU0NTQsImV4cCI6NDg5NTk2NTQ1NH0._9y_wAuVGB6kyzg9-mjIqHuiWzMrExCB41FeJ76mMZs"
    }

    response = requests.request("GET", url, headers=headers)