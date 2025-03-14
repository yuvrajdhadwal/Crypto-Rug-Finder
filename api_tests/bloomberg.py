import blpapi 
from datetime import datetime, timedelta

def fetch_bloomberg_bitcoin_historical(): 
    SERVICE_URI = "//blp/refdata"

    session = blpapi.Session()
    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService(SERVICE_URI):
        print("Failed to open Bloomberg service.")
        return

    service = session.getService(SERVICE_URI)
    request = service.createRequest("HistoricalDataRequest")

    request.append("securities", "XBT Curncy")  # Bitcoin Bloomberg Ticker

    # **Use only fields applicable to historical data**
    fields = [
        "PX_LAST",          # Last Price
        "VOLUME",           # Trading Volume
        "MOV_AVG_50D",      # 50-Day Moving Average
        "MOV_AVG_200D",     # 200-Day Moving Average
        "RETURNS_YTD",      # Year-to-date returns
        "IMPLIED_VOLATILITY_30D"  # Implied volatility (detects price manipulation)
    ]

    for field in fields:
        request.append("fields", field)

    start_date = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")
    end_date = datetime.now().strftime("%Y%m%d")
    request.set("startDate", start_date)
    request.set("endDate", end_date)
    request.set("periodicitySelection", "DAILY")

    print(f"Requesting historical Bitcoin data from {start_date} to {end_date}...")

    session.sendRequest(request)

    while True:
        event = session.nextEvent()
        for msg in event:
            print(msg)

        if event.eventType() == blpapi.Event.RESPONSE:
            break


def fetch_bloomberg_realtime_data():
    SERVICE_URI = "//blp/mktdata"

    session = blpapi.Session()
    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService(SERVICE_URI):
        print("Failed to open Bloomberg market data service.")
        return

    service = session.getService(SERVICE_URI)
    request = service.createRequest("MarketDataRequest")

    request.append("securities", "XBT Curncy")

    # **Fields for real-time scam detection**
    fields = [
        "BID",                 # Highest bid price
        "ASK",                 # Lowest ask price
        "BID_ASK_SPREAD",      # Difference between bid and ask (low liquidity risk)
        "VOLUME",              # Trading volume
        "VWAP",                # Volume Weighted Average Price (detects price manipulation)
        "TURNOVER_RATIO",      # Trading turnover (high turnover may indicate pump-and-dump)
        "OPEN_INTEREST",       # Futures open interest (mass liquidation = scam risk)
        "IMPLIED_VOLATILITY_30D" # 30-day implied volatility
    ]

    for field in fields:
        request.append("fields", field)

    print("Requesting real-time Bitcoin trading data...")

    session.sendRequest(request)

    while True:
        event = session.nextEvent()
        for msg in event:
            print(msg)

        if event.eventType() == blpapi.Event.RESPONSE:
            break

def fetch_bloomberg_crypto_news(): 
    SERVICE_URI = "//blp/news"

    session = blpapi.Session()
    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService(SERVICE_URI):
        print("Failed to open Bloomberg news service.")
        return

    service = session.getService(SERVICE_URI)
    request = service.createRequest("NewsRequest")

    request.append("query", "Bitcoin OR Crypto OR Scam OR Rugpull")  # Search for scam news
    request.set("maxResults", 10)  # Get the latest 10 articles

    print("Requesting latest Bitcoin scam-related news...")

    session.sendRequest(request)

    while True:
        event = session.nextEvent()
        for msg in event:
            print(msg)

        if event.eventType() == blpapi.Event.RESPONSE:
            break

def fetch_bloomberg_whale_insider_data(): 
    SERVICE_URI = "//blp/refdata"

    session = blpapi.Session()
    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService(SERVICE_URI):
        print("Failed to open Bloomberg reference data service.")
        return

    service = session.getService(SERVICE_URI)
    request = service.createRequest("ReferenceDataRequest")

    request.append("securities", "XBT Curncy")  # Bitcoin ticker on Bloomberg

    # Add relevant fields
    fields = [
        "INSIDER_OWNERSHIP",         # % of BTC held by insiders
        "WHALE_TRADES",              # Large whale transactions
        "LOCKUP_EXPIRY_DATE",        # When insider tokens unlock
        "BTC_SUPPLY_HELD_TOP10",     # % of BTC held by top 10 wallets
        "ACTIVE_ADDRESSES",          # Active Bitcoin wallets
        "BLOCKCHAIN_TX_VOLUME",      # Total transaction volume on-chain
        "SUPPLY_CONCENTRATION",      # How centralized Bitcoin supply is
        "SMART_CONTRACT_AUDIT"       # Whether BTC's smart contracts were audited
    ]

    for field in fields:
        request.append("fields", field)

    print("Requesting whale trades, insider ownership, and blockchain activity...")

    session.sendRequest(request)

    while True:
        event = session.nextEvent()
        for msg in event:
            print(msg)

        if event.eventType() == blpapi.Event.RESPONSE:
            break

fetch_bloomberg_whale_insider_data()
# fetch_bloomberg_crypto_news()
# fetch_bloomberg_bitcoin_historical()
# fetch_bloomberg_realtime_data()