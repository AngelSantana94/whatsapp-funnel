import os
import sys

# Allow imports from the project root (lib/) when running on Vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

from lib import db, whatsapp, shopify, messages

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")


@app.route("/api/webhook", methods=["GET"])
def verify():
    """Meta calls this once when you configure the webhook URL."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        # Status updates (sent/delivered/read) have no "messages" key
        incoming_messages = value.get("messages")
        if not incoming_messages:
            return jsonify(status="ignored"), 200

        message = incoming_messages[0]
        wa_id = message["from"]
        msg_type = message.get("type")
        referral = message.get("referral", {})
        referral_source_id = referral.get("source_id")
        came_via_referral = bool(referral)

        if msg_type == "interactive":
            handle_button(wa_id, message["interactive"])
        elif msg_type == "text":
            text_body = message["text"]["body"]
            handle_text(wa_id, text_body, referral_source_id, came_via_referral)
        else:
            # Unsupported message type (image, audio, location...) - ignore,
            # it is neither an ad-entry signal nor a recognizable keyword.
            pass

    except (KeyError, IndexError, TypeError):
        # Malformed/unexpected payload - acknowledge so Meta doesn't retry forever
        pass

    return jsonify(status="ok"), 200


def is_ad_entry(text_body: str, came_via_referral: bool) -> bool:
    """An incoming message counts as an 'ad visit' if Meta attached a
    referral block OR the text matches one of the predefined ad-entry
    messages the customer is instructed to send. Either signal is enough,
    so a missing referral from Meta doesn't break detection."""
    return came_via_referral or text_body.strip() in messages.AD_ENTRY_MESSAGES


def handle_button(wa_id, interactive):
    button_id = interactive.get("button_reply", {}).get("id")

    if button_id == "optin_yes":
        apply_optin_yes(wa_id)
    elif button_id == "optin_no":
        apply_optin_no(wa_id)


def handle_text(wa_id, text_body, referral_source_id, came_via_referral):
    clean = text_body.strip().upper()

    # --- JA / NEE typed as free text (same effect as tapping the buttons) ---
    if clean in messages.YES_KEYWORDS:
        apply_optin_yes(wa_id)
        return

    if clean in messages.NO_KEYWORDS:
        apply_optin_no(wa_id)
        return

    # --- Reactivation: previously opted-out customer types AANMELDEN -------
    if clean == messages.REACTIVATE_KEYWORD:
        db.update_subscriber(
            wa_id, marketing_opt_in=True, opt_in_timestamp=db.now()
        )
        whatsapp.send_text(wa_id, messages.REACTIVATION_REPLY)
        return
    
    

    subscriber = db.get_subscriber(wa_id)
    
    # Returning customer who already opted in — send warm welcome, skip sales flow
    if subscriber and subscriber.get("marketing_opt_in") and is_ad_entry(text_body, came_via_referral):
        whatsapp.send_text(wa_id, messages.RETURNING_OPTIN_CUSTOMER)
        return
    
    # --- New ad visit: first-time customer -----------------------------------
    if subscriber is None:
        if not is_ad_entry(text_body, came_via_referral):
            # Customer messaging us directly without ever coming from an ad.
            # No automated funnel message - a human should pick this up.
            return
        db.create_subscriber(wa_id, referral_source_id)
        whatsapp.send_text(wa_id, messages.get_sales_message(1))
        return

    # --- Customer already purchased: stop pushing discounts -----------------
    if subscriber.get("has_purchased") or shopify.has_purchased(wa_id):
        if not subscriber.get("has_purchased"):
            db.update_subscriber(wa_id, has_purchased=True)
        whatsapp.send_text(wa_id, messages.THANK_YOU_PURCHASED)
        return

    # --- Returning ad visit (2nd, 3rd, 4th, 5th+) ----------------------------
    if is_ad_entry(text_body, came_via_referral):
        visit_count = db.register_ad_visit(wa_id, referral_source_id)
        whatsapp.send_text(wa_id, messages.get_sales_message(visit_count))
        return

    # --- Free-form message from a known subscriber, not an ad re-entry ------
    # Intentionally not handled by the automated funnel - leave it for a
    # human / future logic to pick up.
    return


def apply_optin_yes(wa_id):
    db.update_subscriber(wa_id, marketing_opt_in=True, opt_in_timestamp=db.now())
    whatsapp.send_text(wa_id, messages.OPTIN_YES_REPLY)


def apply_optin_no(wa_id):
    db.update_subscriber(wa_id, marketing_opt_in=False)
    whatsapp.send_text(wa_id, messages.OPTIN_NO_REPLY)


# For local testing: python api/index.py
if __name__ == "__main__":
    app.run(debug=True, port=5000)
