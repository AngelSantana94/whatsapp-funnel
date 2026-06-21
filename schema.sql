-- Run this in the Supabase SQL Editor.
-- Safe to re-run: every statement uses IF NOT EXISTS / OR REPLACE.

create table if not exists subscribers (
  wa_id text primary key,                    -- customer's WhatsApp number
  marketing_opt_in boolean not null default false,
  opt_in_timestamp timestamptz,              -- legal proof of consent (GDPR)
  last_interaction timestamptz default now(),
  contact_count integer not null default 1,  -- which ad-visit number this is
  referral_source_id text,                   -- ad id that originated the visit
  has_purchased boolean not null default false,

  -- 2-hour delayed opt-in question (Stap 2), handled by the cron-triggered
  -- /api/check_pending endpoint instead of a blocking sleep.
  pending_optin_at timestamptz,              -- when the opt-in question should fire
  optin_message_sent boolean not null default false,

  created_at timestamptz default now()
);

-- Used by the webhook to quickly find/skip already-known subscribers
create index if not exists idx_subscribers_opt_in
  on subscribers (marketing_opt_in);

-- Used by /api/check_pending to find due opt-in questions efficiently
create index if not exists idx_subscribers_pending_optin
  on subscribers (pending_optin_at)
  where optin_message_sent = false;
