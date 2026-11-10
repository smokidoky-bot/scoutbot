import json                                                  # JSON-Parser
from pathlib import Path                                     # Dateipfade

from anthropic import beta_tool                              # macht aus einer Funktion ein Werkzeug

from scoutbot.models import Customer                         # unser Kundenformular

CUSTOMERS_FILE = Path(__file__).resolve().parents[2] / "customers.json"   # Pfad zur Kartei: 2 Ordner hoch (scoutbot → src → Projektordner)


def find_customer(customer_id: str) -> Customer | None:      # Suche: Nummer rein → Kunde oder None (= nicht gefunden)
    customers = json.loads(CUSTOMERS_FILE.read_text(encoding="utf-8"))   # Kartei lesen → Liste von Kunden
    for data in customers:                                   # jede Karteikarte durchgehen
        if data["customer_id"] == customer_id:               # passt die Nummer?
            return Customer(**data)                          # ja → als geprüftes Kundenformular zurückgeben
    return None                                              # nichts gefunden


@beta_tool                                                   # ab hier: Werkzeug für den Agenten
def lookup_customer(customer_id: str) -> str:                # Nummer rein → Text raus
    """Look up an Anchorpoint customer by their customer ID.

    Args:
        customer_id: The customer ID from the ticket, e.g. 'C-001'
    """                                                      # ⚠️ Diesen Text liest Claude, um zu verstehen, wofür das Werkzeug da ist
    customer = find_customer(customer_id)                    # in der Kartei suchen
    if customer is None:                                     # nicht gefunden?
        return "No customer found with this ID."             # → klare Meldung an Claude statt Absturz
    return customer.model_dump_json()                        # gefunden → Kundendaten als JSON-Text an Claude