-- Ejecuta esto en el "SQL Editor" de tu proyecto Supabase

create table if not exists subscribers (
  wa_id text primary key,                          -- número de WhatsApp del cliente
  marketing_opt_in boolean not null default false, -- ¿acepta marketing?
  opt_in_timestamp timestamptz,                    -- prueba legal del consentimiento (RGPD)
  last_interaction timestamptz default now(),       -- para controlar la ventana de 24h/72h
  contact_count integer not null default 1,        -- nº de veces que ha entrado vía anuncio
  referral_source_id text,                          -- id del anuncio que originó el contacto
  has_purchased boolean not null default false,    -- si ya compró (vía Shopify)
  created_at timestamptz default now()
);

-- Índice útil para los futuros broadcasts (clientes que dijeron SÍ)
create index if not exists idx_subscribers_opt_in
  on subscribers (marketing_opt_in);
