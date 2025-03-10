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

    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
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

    fetch_bloomberg_bitcoin_historical()

