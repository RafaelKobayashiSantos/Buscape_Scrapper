# Function to get the text content of an element within a card
def get_text(card, selector):

    locator = card.locator(selector)

    if locator.count() > 0:

        texto = locator.text_content()

        return texto.strip() if texto else "N/A"

    return "N/A"

# Scrape the data from the cards and store it in a DataFrame
def scrape_cards(cards, dataFrame):

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

        print(f"Descrição: {description}")
        print(f"Preço: {price}")
        print(f"Link: {link}")
        print(f"URL da Imagem: {image_url}")

        dataFrame["description"].append(description)
        dataFrame["price"].append(price)
        dataFrame["link"].append(link)
        dataFrame["image_url"].append(image_url)


        print(f"Índice {i}")
        print("-" * 50)

    return dataFrame