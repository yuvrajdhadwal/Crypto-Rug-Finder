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



