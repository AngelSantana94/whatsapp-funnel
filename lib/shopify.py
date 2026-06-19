import os
import requests

SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE")  # e.g. "tu-tienda.myshopify.com"
SHOPIFY_ADMIN_TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN")
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-10")


def has_purchased(phone_number):
    """Return True if a Shopify customer with this phone has at least one order.

    Fails silently (returns False) if Shopify isn't configured or the
    request fails, so the bot keeps working even without Shopify set up.
    """
    if not SHOPIFY_STORE or not SHOPIFY_ADMIN_TOKEN:
        return False

    url = f"https://{SHOPIFY_STORE}/admin/api/{SHOPIFY_API_VERSION}/customers/search.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ADMIN_TOKEN}
    # WhatsApp sends numbers without "+", Shopify usually stores them with it
    candidates = {phone_number, f"+{phone_number}"}

    try:
        for candidate in candidates:
            r = requests.get(
                url,
                headers=headers,
                params={"query": f"phone:{candidate}"},
                timeout=5,
            )
            r.raise_for_status()
            customers = r.json().get("customers", [])
            for customer in customers:
                if customer.get("orders_count", 0) > 0:
                    return True
        return False
    except requests.RequestException:
        return False
