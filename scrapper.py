from price_history import get_price_history
import pandas as pd
# Function to get the text content of an element within a card
def get_text(card, selector):

    locator = card.locator(selector)

    if locator.count() > 0:

        texto = locator.text_content()

        return texto.strip() if texto else "N/A"

    return "N/A"

# Scrape the data from the cards and store it in a DataFrame
def scrape_cards(cards, dataFrame, price_historic):

    for i in range(cards.count()):

        card = cards.nth(i)

        description = get_text(
            card,
            '[data-testid="product-card::name"]'
        )

        price = get_text(
            card,
            '[aria-label="Preço"]'
        )

        link = card.locator(
            '[data-area="card"]'
        ).get_attribute("href")

        image_url = card.locator(
            '[data-nimg="fill"]'
        ).get_attribute("src")

        product_id = card.get_attribute("id")

        price_history = get_price_history(int(product_id))
        price_historic.append(price_history)

        print(f"Description: {description}")
        print(f"Price: {price}")
        print(f"Link: {link}")
        print(f"Image URL: {image_url}")
        print(f"Product ID: {product_id}")
        print(f"Price History: {price_history}")

        dataFrame["description"].append(description)
        dataFrame["price"].append(price)
        dataFrame["link"].append(link)
        dataFrame["image_url"].append(image_url)
        dataFrame["product_id"].append(product_id)

        print(f"Índice {i}")
        print("-" * 50)

    return dataFrame, price_historic