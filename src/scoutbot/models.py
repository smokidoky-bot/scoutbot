from typing import Literal                                  # nur feste Werte erlauben

from pydantic import BaseModel, ConfigDict                  # Bauteile fürs Formular


class TriageResult(BaseModel):                              # Formular: Ergebnis einer Ticket-Triage
    model_config = ConfigDict(extra="forbid")               # keine zusätzlichen Felder erlaubt

    category: Literal["billing", "technical", "account", "other"]       # Kategorie (wie bei Jonas)
    priority: Literal["low", "medium", "high"]                          # Priorität als Enum
    suggested_owner: Literal["billing-team", "tech-support", "account-team", "general-support"]  # zuständiges Team