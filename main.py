from playwright.sync_api import sync_playwright
from scrapper import scrape_cards
from pipeline import clean_data
from config import *
import pandas as pd
from request_module import get_price_history, get_product_compare
from product_parser import parse_product_compare
from data_exporter import export_data

dataFrame = {"product_id": [] ,"description": [], "link": [], "price": [], "image_url": []}
price_historic = []
product_details = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=HEADLESS,
    )

    context = browser.new_context(
    viewport=VIEWPORT,
    user_agent=USER_AGENT
    )

    page = context.new_page()

    page.goto(
            BASE_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

    page.wait_for_timeout(WAIT_LOAD)

    n_page = 1

    while n_page <= MAX_PAGES:

        print(f"\n===== PÁGINA {n_page} =====")

        cards = page.locator('[class="Hits_ProductCard__Bonl_"]')

        if cards.count() == 0:
            print("Nenhum anúncio encontrado.")
            break

        dataFrame, price_historic, product_details = scrape_cards(
            cards,
            dataFrame,
            price_historic,
            product_details
        )

        page.mouse.wheel(0, 10000)
        page.wait_for_timeout(WAIT_SCROLL)

        next = page.locator('[data-testid="page-next"]')

        # Break the loop if there is no next page
        if next.count() == 0:
            break
        
        current_url = page.url

        next.click()

        page.wait_for_url(lambda url: url != current_url)

        n_page += 1

# Limpa os dados dos cards
    products = clean_data(dataFrame)

# Exporta as tabelas para o Excel
    export_data(products, price_historic, product_details)

    browser.close()