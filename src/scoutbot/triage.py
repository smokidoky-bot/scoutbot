from anthropic import Anthropic, beta_tool                   # Verbindung zu Claude + Werkzeug-Stempel
from dotenv import load_dotenv                               # liest die .env-Datei

from scoutbot.customers import lookup_customer               # Werkzeug 1: Kunde nachschlagen (Schritt 4)
from scoutbot.models import TriageResult                     # Ergebnis-Formular

load_dotenv()                                                # ANTHROPIC_API_KEY aus .env laden

MODEL = "claude-haiku-4-5"                                   # günstiges, gutes Modell

SYSTEM_PROMPT = (                                            # Etappe 1: Anweisung an Claude
    "You are a support ticket triage assistant for Anchorpoint, a robotics company. "
    "If the ticket has a customer ID, look up the customer first with lookup_customer. "
    "Use the customer's plan and products to set the priority and the team. "
    "Then call submit_triage exactly once with the category, priority, suggested owner "
    "and a short draft reply in the customer's language."
)


def triage(ticket_text: str, customer_id: str | None = None) -> TriageResult:   # Ticket-Text + Kundennummer (darf fehlen) rein → Ergebnis raus
    results = []                                             # hier landet das abgegebene Ergebnis

    @beta_tool                                               # Etappe 2: Werkzeug „Ergebnis abgeben“
    def submit_triage(category: str, priority: str, suggested_owner: str, draft_reply: str) -> str:
        """Submit the final triage result for the ticket.

        Args:
            category: One of billing, technical, account, other
            priority: One of low, medium, high
            suggested_owner: One of billing-team, tech-support, account-team, general-support
            draft_reply: A short, friendly reply to the customer
        """                                                  # Gebrauchsanweisung für Claude, inkl. erlaubter Werte
        result = TriageResult(                               # Werte ins Formular stecken → falscher Wert = Fehler → Claude probiert neu
            category=category,
            priority=priority,
            suggested_owner=suggested_owner,
            draft_reply=draft_reply,
        )
        results.append(result)                               # gültiges Ergebnis merken
        return "Triage result saved."                        # Rückmeldung an Claude

    user_message = f"Customer ID: {customer_id or 'unknown'}\n\nTicket: {ticket_text}"   # Kundennummer (oder „unknown“) + Ticket

    client = Anthropic()                                     # Verbindung zu Claude
    runner = client.beta.messages.tool_runner(               # Etappe 3: Tool Runner = die Agenten-Schleife
        model=MODEL,
        max_tokens=1024,
        max_iterations=5,                                    # höchstens 5 Runden (Schutz vor Endlosschleife)
        system=SYSTEM_PROMPT,                                # Anweisung
        tools=[lookup_customer, submit_triage],              # beide Werkzeuge
        messages=[{"role": "user", "content": user_message}],
    )
    runner.until_done()                                      # Schleife laufen lassen, bis Claude fertig ist

    if not results:                                          # Etappe 4: hat Claude etwas abgegeben?
        raise RuntimeError("The agent did not submit a triage result.")   # nein → klarer Fehler statt Raten
    return results[-1]                                       # ja → das (letzte) gültige Ergebnis zurückgeben