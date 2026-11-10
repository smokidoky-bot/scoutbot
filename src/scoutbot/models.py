from typing import Literal                                  # nur feste Werte erlauben

from pydantic import BaseModel, ConfigDict                  # Bauteile fürs Formular


class TriageResult(BaseModel):                              # Formular: Ergebnis einer Ticket-Triage
    model_config = ConfigDict(extra="forbid")               # keine zusätzlichen Felder erlaubt

    category: Literal["billing", "technical", "account", "other"]       # Kategorie (wie bei Jonas)
    priority: Literal["low", "medium", "high"]                          # Priorität als Enum
    suggested_owner: Literal["billing-team", "tech-support", "account-team", "general-support"]  # zuständiges Team
    draft_reply: str = ""                                    # Antwortentwurf an den Kunden (leer, falls keiner geschrieben wurde)
class Customer(BaseModel):                                   # Formular: ein Kunde
    model_config = ConfigDict(extra="forbid")                # keine zusätzlichen Felder erlaubt

    customer_id: str                                         # z. B. "C-001", ein einfacher Text reicht 
    first_name: str                                          # für die persönliche Anrede in der Antwort
    last_name: str
    email: str                                               # Kontakt
    language: Literal["en", "de", "fr"]                      # Antwort in der richtigen Sprache
    plan: Literal["basic", "premium", "enterprise"]          # Tarif: höher → eher höhere Priorität
    products: list[str]                                      # welche Roboter der Kunde hat, z. B. ["Vacuum X1"]
    customer_since: str                                      # z. B. "2023-04-01", langjährige Kunden sind wichtiger