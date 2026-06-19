import os
from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_supabase = None


def _client():
    global _supabase
    if _supabase is None:
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


def now():
    return datetime.now(timezone.utc).isoformat()


def get_subscriber(wa_id):
    res = _client().table("subscribers").select("*").eq("wa_id", wa_id).execute()
    data = res.data
    return data[0] if data else None


def create_subscriber(wa_id, referral_source_id=None):
    payload = {
        "wa_id": wa_id,
        "marketing_opt_in": False,
        "contact_count": 1,
        "referral_source_id": referral_source_id,
        "has_purchased": False,
        "last_interaction": now(),
    }
    res = _client().table("subscribers").insert(payload).execute()
    return res.data[0] if res.data else payload


def update_subscriber(wa_id, **fields):
    fields["last_interaction"] = now()
    _client().table("subscribers").update(fields).eq("wa_id", wa_id).execute()
