import requests
import os

api_key=os.getenv('MORALIS_API')

params = {
  "network": "mainnet",
  "address": "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt"
}


def get_on_chain_info(chain, address):
    url = "https://solana-gateway.moralis.io/token/mainnet/SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt/pairs"

    headers = {
    "Accept": "application/json",
    "X-API-Key": api_key
    }

    response = requests.request("GET", url, headers=headers)
