import os
import sys

# Allow imports from the project root (lib/) when running on Vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

from lib import db, whatsapp, shopify, messages

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "ziar_verify_2026")


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

        if msg_type == "interactive":
            handle_button(wa_id, message["interactive"])
        elif msg_type == "text":
            handle_text(wa_id, message["text"]["body"], referral_source_id)
        else:
            # Unsupported message type (image, audio, location...) -
            # treat it as a normal interaction for funnel purposes.
            handle_text(wa_id, "", referral_source_id)

    except (KeyError, IndexError, TypeError):
        # Malformed/unexpected payload - acknowledge so Meta doesn't retry forever
        pass

    return jsonify(status="ok"), 200


def handle_button(wa_id, interactive):
    button_id = interactive.get("button_reply", {}).get("id")

    if button_id == "optin_yes":
        db.update_subscriber(
            wa_id, marketing_opt_in=True, opt_in_timestamp=db.now()
        )
        whatsapp.send_text(wa_id, messages.OPTIN_YES_REPLY)

    elif button_id == "optin_no":
        db.update_subscriber(wa_id, marketing_opt_in=False)
        whatsapp.send_text(wa_id, messages.OPTIN_NO_REPLY)


def handle_text(wa_id, text, referral_source_id):
    clean = text.strip().upper()

    # --- Baja explícita (cumplimiento RGPD) ---------------------------------
    if clean in messages.STOP_KEYWORDS:
        db.update_subscriber(wa_id, marketing_opt_in=False)
        whatsapp.send_text(wa_id, messages.STOP_REPLY)
        return

    # --- Re-suscripción ------------------------------------------------------
    if clean == messages.START_KEYWORD:
        db.update_subscriber(
            wa_id, marketing_opt_in=True, opt_in_timestamp=db.now()
        )
        whatsapp.send_text(wa_id, messages.START_REPLY)
        return

    subscriber = db.get_subscriber(wa_id)

    # --- Primer contacto: mensaje de bienvenida + pregunta de opt-in --------
    if subscriber is None:
        db.create_subscriber(wa_id, referral_source_id)
        whatsapp.send_buttons(
            wa_id, messages.MESSAGE_1_BODY, messages.OPTIN_BUTTONS
        )
        return

    # --- Cliente que ya compró: no insistir con descuentos -------------------
    if subscriber.get("has_purchased"):
        whatsapp.send_text(wa_id, messages.THANK_YOU_PURCHASED)
        return

    if shopify.has_purchased(wa_id):
        db.update_subscriber(wa_id, has_purchased=True)
        whatsapp.send_text(wa_id, messages.THANK_YOU_PURCHASED)
        return

    # --- Contactos siguientes: funnel de retargeting (mensajes 2, 3, 4) ------
    count = subscriber.get("contact_count", 1) + 1
    db.update_subscriber(wa_id, contact_count=count)

    if count == 2:
        whatsapp.send_cta_url(
            wa_id, messages.MESSAGE_2_BODY, messages.CTA_TEXT, messages.CTA_URL
        )
    elif count == 3:
        whatsapp.send_cta_url(
            wa_id, messages.MESSAGE_3_BODY, messages.CTA_TEXT, messages.CTA_URL
        )
    else:
        whatsapp.send_cta_url(
            wa_id, messages.MESSAGE_4_BODY, messages.CTA_TEXT, messages.CTA_URL
        )


# Para pruebas locales: python api/index.py
if __name__ == "__main__":
    app.run(debug=True, port=5000)
