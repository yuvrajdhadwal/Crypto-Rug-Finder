# Deploy a Python (Django) web app to Azure App Service - Sample Application

This is the sample Django application for the Azure Quickstart [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python).  For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

* Flask [https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## For local development

Fill in a secret value in the `.env` file.

For local development, use this random string as an appropriate value:

```shell
SECRET_KEY=123abc
```

## When you deploy to Azure

For deployment to production, create an app setting, `SECRET_KEY`. Use this command to generate an appropriate value:

```shell
python -c 'import secrets; print(secrets.token_hex())'
```


    import blpapi

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

fetch_bloomberg_realtime_data()


