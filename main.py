from playwright.sync_api import sync_playwright
from scrapper import scrape_cards
from pipeline import clean_data
from config import *

dataFrame = { "description": [], "link": [], "price": [], "image_url": [] }

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=HEADLESS,
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
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

        dataFrame = scrape_cards(cards, dataFrame)

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

    data = clean_data(dataFrame)
    #process_data(data)

    browser.close()