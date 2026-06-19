# Bot de WhatsApp - Funnel de Suplementos (Python + Vercel + Supabase)

Bot que automatiza el flujo descrito en tus documentos:

1. Primer contacto → mensaje de bienvenida + descuento + pregunta de opt-in (Sí/No).
2. Si dice "Sí" → se guarda el consentimiento (con fecha/hora, válido para RGPD).
3. Si dice "No" o escribe **STOP** → se marca como no-marketing, nunca más recibe mensajes automáticos.
4. Si escribe **START** → se vuelve a suscribir.
5. Contactos siguientes (2º, 3º, 4º+ vía retargeting) → mensajes progresivos (calidad, resultados, garantía).
6. Si el cliente ya compró en Shopify → deja de recibir mensajes de descuento y recibe un mensaje de agradecimiento/soporte.

> Los broadcasts masivos (Fase E del documento) **no** están incluidos en esta primera versión,
> tal y como acordamos. El flujo 1 a 1 vía webhook sí está completo.

---

## 1. Estructura del proyecto

```
whatsapp-funnel-bot/
├── api/
│   └── index.py        # App Flask = punto de entrada del webhook en Vercel
├── lib/
│   ├── db.py            # Conexión y consultas a Supabase
│   ├── whatsapp.py       # Envío de mensajes vía Meta Graph API
│   ├── shopify.py        # Comprobación de compras en Shopify
│   └── messages.py        # Todos los textos del funnel (edítalos aquí)
├── schema.sql            # Tabla de Supabase
├── requirements.txt
├── vercel.json
└── .env.example
```

---

## 2. Crear la base de datos (Supabase, plan gratuito)

1. Crea una cuenta en [supabase.com](https://supabase.com) (gratis).
2. Crea un nuevo proyecto.
3. Ve a **SQL Editor** y pega el contenido de `schema.sql`, ejecútalo.
4. Ve a **Project Settings → API** y copia:
   - `Project URL` → será tu `SUPABASE_URL`
   - `service_role` key → será tu `SUPABASE_KEY` (¡no la "anon"! la service_role tiene permisos de escritura)

El plan gratuito de Supabase (500 MB) es más que suficiente para miles de suscriptores.

---

## 3. Configurar WhatsApp Cloud API (Meta)

1. Entra en [developers.facebook.com](https://developers.facebook.com) y crea una App de tipo "Business".
2. Añade el producto **WhatsApp**. Meta te da automáticamente un número de prueba.
3. En **WhatsApp → API Setup** copia:
   - `Temporary access token` (luego lo cambiaremos por uno permanente)
   - `Phone number ID`
4. Para producción necesitas un **token permanente**: crea un "System User" en
   [Business Settings](https://business.facebook.com/settings) con permiso `whatsapp_business_messaging`
   y genera un token sin caducidad.
5. Verifica tu número de teléfono real y solicita los permisos avanzados de WhatsApp Business
   (Meta puede tardar algunos días en revisarlo).

---

## 4. Configurar Shopify (opcional, ya incluido)

1. En tu panel de Shopify ve a **Settings → Apps and sales channels → Develop apps**.
2. Crea una app personalizada.
3. En **Admin API access scopes** activa `read_customers` y `read_orders`.
4. Instala la app y copia el **Admin API access token** → será tu `SHOPIFY_ADMIN_TOKEN`.
5. `SHOPIFY_STORE` es el dominio `.myshopify.com` de tu tienda.

Si no rellenas estas variables, el bot simplemente ignora la comprobación de Shopify
(no falla, solo no la usa).

---

## 5. Desplegar en Vercel (plan gratuito)

1. Sube este proyecto a un repositorio de GitHub.
2. Entra en [vercel.com](https://vercel.com) → **New Project** → importa el repo.
3. Vercel detectará `vercel.json` y usará el runtime de Python automáticamente.
4. En **Settings → Environment Variables**, añade todas las variables de `.env.example`
   con tus valores reales.
5. Haz "Deploy". Tu webhook quedará en:
   ```
   https://tu-proyecto.vercel.app/api/webhook
   ```

---

## 6. Conectar el webhook con Meta

1. En tu App de Meta, ve a **WhatsApp → Configuration**.
2. En "Webhook", pon:
   - **Callback URL**: `https://tu-proyecto.vercel.app/api/webhook`
   - **Verify token**: el mismo valor que pusiste en `VERIFY_TOKEN`
3. Pulsa "Verify and save". Meta hará una petición GET que tu app responde automáticamente.
4. En "Webhook fields", suscríbete a `messages`.

¡Listo! Cualquier mensaje que llegue a tu número de WhatsApp Business activará el flujo.

---

## 7. Probar en local (opcional)

```bash
pip install -r requirements.txt
export $(cat .env | xargs)   # o usa python-dotenv
python api/index.py
```

Para probar webhooks entrantes en local puedes usar [ngrok](https://ngrok.com) y apuntar
la "Callback URL" de Meta a la URL pública que te da ngrok.

---

## 8. Edición de textos

Todos los mensajes (descuentos, textos de opt-in, mensajes 2/3/4, etc.) están en
`lib/messages.py`. Puedes cambiarlos sin tocar la lógica del bot.

---

## 9. Cumplimiento legal (RGPD + políticas de Meta)

El bot ya implementa los puntos clave de tus documentos:

- **Opt-in explícito y registrado** con fecha/hora (`opt_in_timestamp`) → prueba legal (art. 7 RGPD).
- **STOP / START** funcionan como baja y re-suscripción inmediatas.
- Si el cliente dice "No", **nunca** se le vuelve a enviar marketing automático.
- No se procesan ni almacenan datos sensibles (solo número de WhatsApp y estado de opt-in).

Recuerda igualmente publicar una política de privacidad en tu web que explique este uso de datos.

---

## 10. Próximos pasos (no incluidos todavía)

- **Broadcasts masivos**: cuando lo necesites, se puede añadir un endpoint
  `/api/broadcast` protegido por una clave secreta, que recorra los
  `marketing_opt_in = true` y envíe una plantilla aprobada por Meta. Lo dejamos
  fuera de esta versión porque pediste centrarte primero en el flujo 1 a 1.
- **Plantillas (Templates) aprobadas por Meta**: necesarias para enviar mensajes
  fuera de la ventana de 24h. Se crean desde el WhatsApp Manager de Meta.
