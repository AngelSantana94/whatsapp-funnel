import os
from datetime import datetime, timedelta, timezone
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

OPTIN_DELAY_HOURS = 2  # matches the "wachttijd van exact 2 uur" in the docs

_supabase = None


def _client():
    global _supabase
    if _supabase is None:
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


def now():
    return datetime.now(timezone.utc).isoformat()


def now_plus_optin_delay():
    return (datetime.now(timezone.utc) + timedelta(hours=OPTIN_DELAY_HOURS)).isoformat()


def get_subscriber(wa_id):
    res = _client().table("subscribers").select("*").eq("wa_id", wa_id).execute()
    data = res.data
    return data[0] if data else None


def create_subscriber(wa_id, referral_source_id=None):
    """Creates a brand-new subscriber on their first ad visit and schedules
    the Stap 2 opt-in question for 2 hours from now."""
    payload = {
        "wa_id": wa_id,
        "marketing_opt_in": False,
        "contact_count": 1,
        "referral_source_id": referral_source_id,
        "has_purchased": False,
        "last_interaction": now(),
        "pending_optin_at": now_plus_optin_delay(),
        "optin_message_sent": False,
    }
    res = _client().table("subscribers").insert(payload).execute()
    return res.data[0] if res.data else payload


def update_subscriber(wa_id, **fields):
    fields["last_interaction"] = now()
    _client().table("subscribers").update(fields).eq("wa_id", wa_id).execute()


def register_ad_visit(wa_id, referral_source_id=None):
    """Called every time the customer enters via an ad (matched by referral
    payload or by sending one of the AD_ENTRY_MESSAGES). Increments the
    visit counter and re-schedules the Stap 2 opt-in question 2h out."""
    new_count = _client().table("subscribers").select("contact_count") \
        .eq("wa_id", wa_id).execute().data[0]["contact_count"] + 1
    update_subscriber(
        wa_id,
        contact_count=new_count,
        referral_source_id=referral_source_id,
        pending_optin_at=now_plus_optin_delay(),
        optin_message_sent=False,
    )
    return new_count


def get_due_optin_subscribers():
    """Used by /api/check_pending — returns subscribers whose 2h wait is
    over and who haven't received their Stap 2 message yet."""
    res = (
        _client()
        .table("subscribers")
        .select("*")
        .eq("optin_message_sent", False)
        .lte("pending_optin_at", now())
        .execute()
    )
    return res.data or []
