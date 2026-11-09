from anthropic import Anthropic                              # Verbindung zu Claude
from dotenv import load_dotenv                               # liest die .env-Datei

from scoutbot.models import TriageResult                     # unser Formular aus Schritt 4

load_dotenv()                                                # ANTHROPIC_API_KEY aus .env laden (nicht mehr im Code!)

MODEL = "claude-haiku-4-5"                                   # günstiges, gutes Modell (wie bei Jonas)

SYSTEM_PROMPT = (                                            # Rolle und Aufgabe getrennt vom Ticket (Checkliste: system + user trennen)
    "You are a support ticket triage assistant for Anchorpoint. "
    "Classify the customer's ticket with the triage_ticket tool."
)

TRIAGE_TOOL = {                                              # das Werkzeug, das Claude „aufrufen“ soll
    "name": "triage_ticket",                                 # Name des Werkzeugs
    "description": "Record the category, priority and responsible team of a support ticket.",  # wofür es da ist
    "strict": True,                                          # Leitplanken an: Antwort MUSS zum Schema passen
    "input_schema": TriageResult.model_json_schema(),        # das Formular als Bauplan
}


def triage(ticket_text: str) -> TriageResult:                # Funktion: Ticket-Text rein → geprüftes Ergebnis raus
    client = Anthropic()                                     # Verbindung erst hier aufbauen (gut für Tests später)
    response = client.messages.create(                       # Anfrage an Claude
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,                                # Rolle und Regeln
        messages=[{"role": "user", "content": ticket_text}], # nur das Ticket als user-Nachricht
        tools=[TRIAGE_TOOL],                                 # erlaubtes Werkzeug
        tool_choice={"type": "tool", "name": "triage_ticket"},  # Claude MUSS genau dieses Werkzeug benutzen
    )
    tool_use = next(block for block in response.content if block.type == "tool_use")  # den Tool-Aufruf aus der Antwort heraussuchen
    return TriageResult.model_validate(tool_use.input)       # Argumente ins Formular füllen und prüfen