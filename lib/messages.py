# -----------------------------------------------------------------------
# All customer-facing copy lives here, in Dutch (NL), exactly as provided
# by the client in their 5 source documents. Variable/field names stay in
# English so the codebase remains maintainable by any future developer.
#
# Edit ONLY the text values below. Do not rename the dict keys unless you
# also update every place in api/index.py and api/check_pending.py that
# references them.
# -----------------------------------------------------------------------

WEBSHOP_LINK = "https://www.ziarnutrition.com"          # replace with the real shop URL
DISCOUNT_CODE = "ZIAR10"

# =========================================================================
# AD ENTRY DETECTION
# -------------------------------------------------------------------------
# Predefined message(s) the client is instructed to send when entering
# WhatsApp via a Meta ad (Click-to-WhatsApp). Used together with the
# `referral` payload field to reliably detect "ad visit" vs "free-form
# customer message". Add new variants here as new ad campaigns are created
# — never delete old ones, just extend the set.
# =========================================================================
AD_ENTRY_MESSAGES = {
    "Hoi, ik wil graag meer weten over...",
}

# =========================================================================
# STEP 1 — SALES MESSAGE PER VISIT NUMBER (sent immediately on ad entry)
# -------------------------------------------------------------------------
# Keys = contact_count value at the time of entry.
# 5 covers "5th visit and beyond" (every count >= 5 reuses this message).
# =========================================================================
SALES_MESSAGE_BY_VISIT = {
    1: (
        "Welkom bij ZiarNutrition 👋\n"
        "Jouw partner voor een gezonde en fitte levensstijl.\n\n"
        "Zoek je de beste supplementen om jouw doelen te bereiken?\n"
        "Op onze webshop vind je ons volledige assortiment, inclusief "
        "productinformatie en reviews.\n\n"
        "🛒 Shop direct via: https://www.ziarnutrition.com\n\n"
        "🎁 Als welkomstcadeau ontvang je vandaag 10% korting op je "
        "eerste bestelling met de code: ZIAR10"
    ),
    2: (
        "Ben je nog steeds op zoek naar de juiste ondersteuning voor jouw sportdoelen?\n"
        "Twijfel je welke supplementen echt bij je passen?\n\n"
        "Het is zonde om je harde werk te laten remmen door energiedips of supplementen van lage kwaliteit.\n\n"
        "Ons doel is simpel:\n"
        "✅ Kwalitatieve supplementen\n"
        "✅ Transparante ingrediënten\n"
        "✅ Ondersteuning voor jouw sportdoelen\n\n"
        "Ervaar zelf het verschil en ontdek ons assortiment.\n\n"
        "🛒 Bekijk alle producten en reviews:\n"
        "https://www.ziarnutrition.com\n\n"
        "🎁 Je welkomstkorting staat nog steeds voor je klaar:\n"
        "Gebruik code ZIAR10 voor 10% korting op je bestelling."
    ),
    3: (
        "Welkom terug bij ZiarNutrition! 👋\n"
        "Je bent duidelijk serieus bezig met je sportdoelen.\n\n"
        "Twijfel je nog over welke supplementen het beste bij jou passen?\n"
        "Of zoek je ondersteuning zonder onnodige of vage toevoegingen?\n\n"
        "Het is zonde als energiedips of matige kwaliteit je vooruitgang afremmen.\n\n"
        "Ons doel blijft helder:\n"
        "✅ Kwalitatieve supplementen\n"
        "✅ Transparante ingrediënten\n"
        "✅ Ondersteuning voor échte resultaten\n\n"
        "Kies vandaag voor kwaliteit en ontdek ons assortiment.\n\n"
        "🛒 Shop direct via:\n"
        "https://www.ziarnutrition.com\n\n"
        "⏳ Laatste kans:\n"
        "Je 10% welkomstkorting staat nog voor je klaar met code: ZIAR10"
    ),
    4: (
        "Welkom terug bij ZiarNutrition! 👋\n"
        "Je hebt onze producten inmiddels al meerdere keren bekeken.\n\n"
        "Het is duidelijk dat je serieus bezig bent met jouw sportdoelen.\n"
        "Waarom genoegen nemen met energiedips of supplementen van matige kwaliteit?\n\n"
        "Ons doel is simpel:\n"
        "✅ Zuivere ingrediënten\n"
        "✅ Hoge kwaliteit\n"
        "✅ Ondersteuning voor jouw prestaties\n\n"
        "Zet vandaag de volgende stap en ontdek wat bij jouw doelen past.\n\n"
        "🛒 Bestel direct via:\n"
        "https://www.ziarnutrition.com\n\n"
        "⏳ Let op:\n"
        "Dit is je laatste kans om code ZIAR10 te gebruiken voor 10% korting op je eerste bestelling."
    ),
    5: (
        "Welkom terug bij ZiarNutrition! 👋\n"
        "Je bent duidelijk bezig met je gezondheid en sportdoelen.\n\n"
        "Ben je nog op zoek naar de juiste ondersteuning?\n"
        "Dan ben je bij ZiarNutrition aan het juiste adres.\n\n"
        "Ons doel is simpel:\n"
        "✅ Kwalitatieve supplementen\n"
        "✅ Transparante ingrediënten\n"
        "✅ Ondersteuning voor jouw sportieve doelen\n\n"
        "Ontdek ons assortiment en ervaar zelf het verschil.\n\n"
        "🛒 Shop direct via:\n"
        "https://www.ziarnutrition.com\n\n"
        "🎁 Je 10% welkomstkorting staat nog steeds voor je klaar:\n"
        "ZIAR10"
    ),
}

MAX_DEFINED_VISIT = max(SALES_MESSAGE_BY_VISIT.keys())  # = 5


def get_sales_message(visit_count: int) -> str:
    """Returns the right sales copy for a given visit number.
    Any visit_count beyond MAX_DEFINED_VISIT reuses the 5th-visit copy."""
    key = min(visit_count, MAX_DEFINED_VISIT)
    return SALES_MESSAGE_BY_VISIT[key]


# =========================================================================
# STEP 2 — OPT-IN QUESTION PER VISIT NUMBER (sent 2h after the sales msg)
# =========================================================================
OPTIN_QUESTION_BY_VISIT = {
    1: (
        "Hi! 👋\n\n"
        "We hopen dat je een goede eerste indruk hebt gekregen van onze webshop en onze missie.\n\n"
        "Omdat je nieuw bent bij Ziar Nutrition, vinden we het leuk om je te inspireren met:\n\n"
        "💪 Handige sporttips en updates over onze producten\n"
        "🎁 Exclusieve acties en kortingen\n\n"
        "Mogen we je af en toe een WhatsApp-bericht sturen?\n\n"
        "Antwoord met JA of NEE (of gebruik de knoppen hieronder)."
    ),
    2: (
        "Hi! 👋\n\n"
    "Je hebt onze webshop al een tweede keer bezocht.\n\n"
    "We zouden het leuk vinden om je op de hoogte te houden van:\n\n"
    "💪 Handige sporttips en updates over onze producten\n"
    "🎁 Exclusieve acties en kortingen\n\n"
    "Zo mis je geen enkele update of voordeel.\n\n"
    "Mogen we je af en toe een WhatsApp-bericht sturen?\n\n"
    "Antwoord met JA of NEE (of gebruik de knoppen hieronder)."
    ),
    3: (
        "Hi! 👋\n\n"
    "Je hebt inmiddels een goed beeld van onze webshop en wat we voor "
    "jouw doelen kunnen betekenen.\n\n"
    "Daarom willen we je graag als eerste op de hoogte houden van:\n\n"
    "🎁 Exclusieve kortingsacties\n"
    "🚀 Nieuwe producten en voorraden\n"
    "💪 Handige sport- en gezondheidstips\n\n"
    "Zo mis je geen belangrijke updates of voordelen.\n\n"
    "Mogen we je af en toe een WhatsApp-bericht sturen?\n\n"
    "Antwoord met JA of NEE (of gebruik de knoppen hieronder)."
    ),
    4: (
            "Hi! 👋\n\n"
    "We zien dat je regelmatig interesse toont in onze producten.\n\n"
    "Daarom nodigen we je graag uit voor onze exclusieve VIP-lijst.\n\n"
    "Als VIP ontvang je als eerste:\n\n"
    "🎁 Exclusieve kortingsacties en Vroegtijdige toegang tot nieuwe producten\n"
    "💪 Handige sport- en gezondheidstips\n\n"
    "Zo mis je geen enkele update of voordeel.\n\n"
    "Mogen we je af en toe een WhatsApp-bericht sturen?\n\n"
    "Antwoord met JA of NEE (of gebruik de knoppen hieronder)."
    ),
    5: (
        "Hi! 👋\n\n"
    "Je bent inmiddels één van onze meest actieve bezoekers.\n\n"
    "Daarom nodigen we je graag uit voor onze exclusieve binnencirkel.\n\n"
    "Als lid ontvang je als eerste:\n\n"
    "🎁 Exclusieve kortingsacties\n"
    "🚀 Vroege toegang tot nieuwe producten\n"
    "💪 Handige sport- en gezondheidstips\n\n"
    "Zo mis je geen enkele update of voordeel.\n\n"
    "Mogen we je af en toe een WhatsApp-bericht sturen?\n\n"
    "Antwoord met JA of NEE (of gebruik de knoppen hieronder)."
    ),
}


def get_optin_question(visit_count: int) -> str:
    key = min(visit_count, MAX_DEFINED_VISIT)
    return OPTIN_QUESTION_BY_VISIT[key]


# Button labels shown under the opt-in question (interactive message)
OPTIN_BUTTONS = [
    ("optin_yes", "JA"),
    ("optin_no", "NEE"),
]

# =========================================================================
# STEP 3 — REPLY AFTER THE CUSTOMER CHOOSES (same text for every visit#)
# =========================================================================
OPTIN_YES_REPLY = (
    "Geweldig! 🎉\n\n"
    "Tof dat we je mogen updaten en af en toe een appje mogen sturen met "
    "nieuws over onze producten en handige gezonde tips.\n\n"
    "Je hoeft nu niets meer te doen.\n\n"
    f"🎁 Vergeet niet je 10% welkomstkorting te gebruiken met de code:\n"
    f"{DISCOUNT_CODE}\n\n"
    "🛒 Veel succes met shoppen op onze webshop!\n\n"
    "❓ Heb je vragen of wil je persoonlijk advies over onze producten? "
    "Stuur ons gerust een WhatsApp-bericht via +31 6 15717980. "
    "We helpen je graag verder.\n\n"
    "Tot snel! 👋"
)

OPTIN_NO_REPLY = (
    "Jammer, maar dat respecteren we natuurlijk volledig. 😊\n\n"
    "Geen zorgen, we zullen je geen berichten meer sturen.\n\n"
    "Verander je in de toekomst van gedachten?\n"
    "Stuur dan simpelweg AANMELDEN en we sturen je opnieuw updates.\n\n"
    f"🎁 Je kunt nog steeds gebruikmaken van je 10% welkomstkorting.\n\n"
    f"🛒 Shop hier: {WEBSHOP_LINK}\n\n"
    "❓ Heb je nog vragen of wil je persoonlijk advies? "
    "Je kunt ons altijd een WhatsApp-bericht sturen via +31 6 15717980. "
    "We helpen je graag verder.\n\n"
    "Veel plezier met shoppen en misschien tot later! 👋"
)

# =========================================================================
# STEP 4 — REACTIVATION (customer who said NEE later types AANMELDEN)
# =========================================================================
REACTIVATION_REPLY = (
    "Hey! 👋\n\n"
    "Wat tof dat je er weer bij bent!\n\n"
    "Vanaf nu houden we je opnieuw op de hoogte van:\n\n"
    "💪 Gezonde tips, sportadvies en updates over onze producten\n"
    "🎁 Exclusieve acties en kortingen\n\n"
    "Welkom terug bij de ZiarNutrition-community!\n\n"
    "Fijn dat je weer van de partij bent. 😊"
)

# =========================================================================
# Free-text keyword recognition (Dutch). Customer can type these instead
# of tapping the interactive buttons.
# =========================================================================
YES_KEYWORDS = {"JA"}
NO_KEYWORDS = {"NEE"}
REACTIVATE_KEYWORD = "AANMELDEN"

# =========================================================================
# Customer who already purchased (checked via Shopify) — no more discount
# pushes, just a friendly support-oriented message.
# =========================================================================
THANK_YOU_PURCHASED = (
    "Fijn dat je al bij ons hebt besteld! Heb je vragen over je bestelling "
    "of het gebruik van je supplementen? Laat het ons gerust weten, we "
    "helpen je graag verder."
)

# Returning customer with OPT-IN TRUE — skip the cold sales flow entirely
RETURNING_OPTIN_CUSTOMER = (
    "Welkom terug! 👋\n\n"
    "Leuk dat je er weer bent.\n\n"
    "Bekijk direct onze nieuwste producten en ontdek welke aanbieding "
    "vandaag het beste bij jou past.\n\n"
    f"🛒 {WEBSHOP_LINK}"
)
