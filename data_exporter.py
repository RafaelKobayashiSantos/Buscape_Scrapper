
import json
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("PBI")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_data(dataFrame, price_historic, product_details):
    # 1. Produtos coletados dos cards
    products_df = pd.DataFrame(dataFrame).copy()

    # 2. Histórico: transforma listas de históricos em linhas
    history_rows = []

    for product_history in price_historic:
        if isinstance(product_history, list):
            records = product_history
        elif isinstance(product_history, dict):
            records = [product_history]
        else:
            continue

        for item in records:
            if isinstance(item, dict):
                history_rows.append({
                    "product_id": item.get("product_id"),
                    "date": item.get("date"),
                    "price": item.get("price")
                })

    history_df = pd.DataFrame(
        history_rows,
        columns=["product_id", "date", "price"]
    )

    # 3. Detalhes: aceita tanto dicionário quanto lista
    if isinstance(product_details, dict):
        details = list(product_details.values())
    else:
        details = list(product_details)

    product_rows = []
    specification_rows = []

    for product in details:
        if not isinstance(product, dict):
            continue

        offer = product.get("best_offer") or {}

        product_rows.append({
            "product_id": product.get("product_id"),
            "name": product.get("name"),
            "url_path": product.get("url_path"),
            "rating": product.get("rating"),
            "review_count": product.get("review_count"),
            "best_offer_price": offer.get("price"),
            "best_offer_total_price": offer.get("total_price"),
            "best_offer_seller": offer.get("seller"),
            "best_offer_seller_id": offer.get("seller_id"),
            "seller_count": offer.get("seller_count"),
            "condition": offer.get("condition"),
            "images": json.dumps(
                product.get("images", []),
                ensure_ascii=False
            )
        })

        # Converte especificações aninhadas em linhas
        specifications = product.get("specifications") or {}

        for group, attributes in specifications.items():
            for attribute, values in attributes.items():
                if not isinstance(values, list):
                    values = [values]

                for value in values:
                    if isinstance(value, dict):
                        specification_rows.append({
                            "product_id": product.get("product_id"),
                            "group": group,
                            "attribute": attribute,
                            "value": value.get("value"),
                            "unit": value.get("unit")
                        })

    details_df = pd.DataFrame(product_rows)

    specifications_df = pd.DataFrame(
        specification_rows,
        columns=[
            "product_id",
            "group",
            "attribute",
            "value",
            "unit"
        ]
    )

    # Exporta tudo para um único arquivo Excel
    output_file = OUTPUT_DIR / "buscape_data.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        products_df.to_excel(
            writer, sheet_name="Products", index=False
        )
        history_df.to_excel(
            writer, sheet_name="PriceHistory", index=False
        )
        details_df.to_excel(
            writer, sheet_name="ProductDetails", index=False
        )
        specifications_df.to_excel(
            writer, sheet_name="Specifications", index=False
        )

    print(f"Dados exportados para: {output_file}")
