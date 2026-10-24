
import requests
import random
import time

def get_product_compare(product_id):
    api_url = (
        "https://api-v1.zoom.com.br/restql/run-query/"
        f"spotlight/product_compare/1?tenant=DEFAULT&product_id={product_id}"
    )

    time.sleep(random.uniform(0.8, 1.4))

    response = requests.get(api_url, timeout=30)
    response.raise_for_status()

    return response.json()

def get_price_history(product_id, months=12):
    """
    Extrai o histórico de preços de um produto.
    """
    api_url = (
        "https://api-v1.zoom.com.br/restql/run-query/"
        f"sherlock/product_price_history/1?"
        f"tenant=DEFAULT&product_id={product_id}"
        f"&period=months&amount={months}"
    )

    time.sleep(random.uniform(0.8, 1.4))

    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    data = response.json()

    history = data["product_price_history"]["result"]

    return {
        str(product_id): [
            {
                "date": item["date"],
                "price": item["price"]
            }
            for item in history
        ]
    }
