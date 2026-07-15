import requests
import random
import time
from datetime import datetime, timedelta
import pandas as pd

def get_price_history(product_id, months=12):
    """
    Fetches the price history for a given product ID over a specified number of months.

    Args:
        product_id (int): The ID of the product to fetch price history for.
        months (int): The number of months to look back for price history.

    Returns:
        dict: The price history data for the specified product.
    """
    api_url = f"https://api-v1.zoom.com.br/restql/run-query/sherlock/product_price_history/1?tenant=DEFAULT&product_id={product_id}&period=months&amount={months}"

    time.sleep(random.uniform(0.8, 1.4))  # Simulate a delay
    response = requests.get(api_url).json()

    history = response["product_price_history"]["result"]

    return [
        {
            "product_id": item["prodId"],
            "date": item["date"],
            "price": item["price"]
        }
        for item in history
    ]