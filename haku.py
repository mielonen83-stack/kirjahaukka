import os
import sys
import requests

# --- Asetukset ---------------------------------------------------
# Toimii kahdella tavalla:
# 1) Paikallisesti: kirjoita token ja chat_id alle suoraan
# 2) GitHub Actionsissa: arvot tulevat ympäristömuuttujista (secrets)
TOKEN = os.environ.get("TELEGRAM_TOKEN", "LIITA_TOKEN_TAHAN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "LIITA_CHAT_ID_TAHAN")


# --- Finna-haku --------------------------------------------------
def finna_haku(isbn: str) -> list:
    """Hakee kirjan tiedot Finna-rajapinnasta ISBN:llä."""
    r = requests.get(
        "https://api.finna.fi/api/v1/search",
        params={
            "lookfor": f'isbn:"{isbn}"',
            "type": "AllFields",
            "field[]": ["title", "publishDate", "publisher", "authors"],
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json().get("records", [])


# --- Telegram ----------------------------------------------------
def telegram_laheta(teksti: str):
    """Lähettää viestin Telegram-bottisi kautta."""
    r = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"
