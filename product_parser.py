
from itertools import product


def parse_product_compare(data):
    product = data["product"]["result"]
    print("COMMENT:", repr(product.get("comment")))
    print("TIPO:", type(product.get("comment")))

    best_offer = product.get("offer", {}).get("bestOffer", {})
    sales = best_offer.get("sales_condition", {})
    seller = best_offer.get("seller", {})

    # Extrair as especificações técnicas
    specifications = {}

    for group in product.get("specification", {}).get("attributes", []):
        group_name = group.get("group", "Outros")
        specifications[group_name] = {}

        for attribute in group.get("values", []):
            name = attribute.get("name")

            values = [
                {
                    "value": value.get("name"),
                    "unit": value.get("unit")
                }
                for value in attribute.get("values", [])
                if value.get("show", False)
            ]

            if name and values:
                specifications[group_name][name] = values

    # Extrair imagens com segurança
    images = []

    for image in product.get("images", []):
        embedded = image.get("_embedded", {})
        image_data = embedded.get("zoom_rels:images", [])

        if image_data:
            urls = image_data[0].get("urls")

            if urls:
                images.append(urls)

    # Organizar os dados do produto
    return {
        "product_id": product.get("id"),
        "name": product.get("name"),
        "url_path": product.get("routes", {}).get("canonical"),
        "images": images,
        "rating": (
            product.get("comment", {}).get("rating")
            if isinstance(product.get("comment"), dict)
            else None
        ),
        "review_count": (
            product.get("comment", {}).get("countOfComments")
            if isinstance(product.get("comment"), dict)
            else None
        ),
        "best_offer": {
            "offer_id": best_offer.get("offer_id"),
            "price": sales.get("price"),
            "total_price": sales.get("total_price"),
            "seller": seller.get("name"),
            "seller_id": seller.get("id"),
            "seller_count": product.get("offer", {}).get(
                "seller_count"
            ),
            "condition": best_offer.get("condition")
        },
        "specifications": specifications
    }
