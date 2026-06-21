import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

from lib import db, whatsapp, messages

app = Flask(__name__)

# Shared secret so random people on the internet can't trigger this endpoint.
# Set this in Vercel env vars and use the same value as a query param in
# your cron-job.org request, e.g.:
#   https://your-app.vercel.app/api/check_pending?key=YOUR_CRON_SECRET
CRON_SECRET = os.environ.get("CRON_SECRET")


@app.route("/api/check_pending", methods=["GET", "POST"])
def check_pending():
    if CRON_SECRET and request.args.get("key") != CRON_SECRET:
        return "Forbidden", 403

    due = db.get_due_optin_subscribers()
    sent = 0

    for subscriber in due:
        wa_id = subscriber["wa_id"]
        visit_count = subscriber.get("contact_count", 1)

        whatsapp.send_buttons(
            wa_id,
            messages.get_optin_question(visit_count),
            messages.OPTIN_BUTTONS,
        )
        db.update_subscriber(wa_id, optin_message_sent=True)
        sent += 1

    return jsonify(status="ok", sent=sent), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
