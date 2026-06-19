import os
import requests

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
GRAPH_VERSION = os.environ.get("GRAPH_VERSION", "v21.0")

BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"


def _headers():
    return {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }


def send_text(to, body):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }
    return requests.post(BASE_URL, headers=_headers(), json=payload, timeout=10)


def send_buttons(to, body_text, buttons):
    """buttons: list of (id, title) tuples, max 3 items, title max 20 chars"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": bid, "title": title}}
                    for bid, title in buttons
                ]
            },
        },
    }
    return requests.post(BASE_URL, headers=_headers(), json=payload, timeout=10)


def send_cta_url(to, body_text, button_text, url):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "body": {"text": body_text},
            "action": {
                "name": "cta_url",
                "parameters": {"display_text": button_text, "url": url},
            },
        },
    }
    return requests.post(BASE_URL, headers=_headers(), json=payload, timeout=10)
