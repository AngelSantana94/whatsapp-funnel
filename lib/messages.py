# -----------------------------------------------------------------------
# Textos del funnel. Edita libremente el contenido, pero respeta el
# formato de las variables (CTA_URL, listas de botones, etc.)
# -----------------------------------------------------------------------

BRAND_NAME = "Ziar Nutrition"
CTA_URL = "https://tutienda.com"
CTA_TEXT = "Comprar con descuento"
DISCOUNT_CODE = "WELKOM10"

# --- Mensaje 1: primer contacto + pregunta de opt-in -----------------------
MESSAGE_1_BODY = (
    f"¡Bienvenido/a a {BRAND_NAME}! 👋 Qué bien que nos escribas. "
    f"Para empezar con buen pie, aquí tienes un 10% de descuento en tu "
    f"primer pedido con el código: {DISCOUNT_CODE} ⚡\n\n"
    "Nos encantaría enviarte de vez en cuando ofertas y novedades por "
    "WhatsApp, ¿te apetece?"
)

OPTIN_BUTTONS = [
    ("optin_yes", "Sí, genial ✅"),
    ("optin_no", "No, gracias"),
]

# --- Respuestas a los botones de opt-in ------------------------------------
OPTIN_YES_REPLY = (
    "¡Genial! 🙌 A partir de ahora serás de los primeros en enterarte de "
    "nuestras novedades y descuentos. Prometemos no saturar tu chat, solo "
    f"lo realmente interesante. ¡Disfruta de tu código {DISCOUNT_CODE}!"
)

OPTIN_NO_REPLY = (
    "¡Sin problema! 👍 Puedes usar igualmente el código "
    f"{DISCOUNT_CODE} en tu pedido. Si más adelante cambias de opinión, "
    "escríbenos la palabra START."
)

# --- STOP / START ------------------------------------------------------------
STOP_KEYWORDS = {"STOP", "BAJA", "AFMELDEN", "PARAR", "CANCELAR"}
START_KEYWORD = "START"

STOP_REPLY = (
    "Te has dado de baja correctamente. No volverás a recibir mensajes de "
    "marketing por nuestra parte. Si quieres volver a suscribirte, "
    "escribe START en cualquier momento."
)

START_REPLY = (
    "¡Qué bien tenerte de vuelta! 🎉 Te hemos vuelto a suscribir a nuestras "
    "novedades y ofertas."
)

# --- Mensajes 2, 3 y 4: retargeting -----------------------------------------
SUPP_DISCOUNT_CODE = "SUPP10"

MESSAGE_2_BODY = (
    "¡Bienvenido/a de nuevo! Cuando se trata de tu cuerpo, quieres solo lo "
    "mejor. Nuestros suplementos son 100% puros, con respaldo científico y "
    f"sin rellenos innecesarios. Tu código {SUPP_DISCOUNT_CODE} sigue activo 👇"
)

MESSAGE_3_BODY = (
    "¡Bienvenido/a otra vez! ¿Sabías que más del 85% de nuestros clientes "
    "nota un cambio claro en su energía y vitalidad en solo 3 semanas? "
    f"Tu código personal {SUPP_DISCOUNT_CODE} te está esperando 👇"
)

MESSAGE_4_BODY = (
    "¡Bienvenido/a de nuevo! Entendemos que quieras estar seguro/a antes de "
    "comprar. Por eso lo hacemos fácil: pruébalo 30 días, y si no notas "
    f"diferencia, te devolvemos el dinero. Usa tu código {SUPP_DISCOUNT_CODE} "
    "hoy mismo y empieza sin riesgo 👇"
)

# --- Cliente que ya compró ----------------------------------------------------
THANK_YOU_PURCHASED = (
    "¡Genial, vemos que ya hiciste tu pedido! 🎉 Si tienes dudas sobre cómo "
    "tomar tus suplementos o sobre tu envío, aquí estamos para ayudarte."
)
