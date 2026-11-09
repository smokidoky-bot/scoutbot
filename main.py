import argparse                                              # Eingaben von der Kommandozeile lesen
import json                                                  # der JSON-Parser („Übersetzer“)
from pathlib import Path                                     # Dateipfade

from scoutbot.triage import triage                           # unsere Triage-Funktion aus Schritt 5


def main() -> None:                                          # Hauptprogramm
    parser = argparse.ArgumentParser(description="Triage Anchorpoint support tickets.")   # Kommandozeilen-Programm beschreiben
    parser.add_argument("tickets_file", nargs="?", default="sample_tickets.json")        # Datei optional angeben, Standard: sample_tickets.json
    args = parser.parse_args()                               # Eingaben auslesen

    tickets = json.loads(Path(args.tickets_file).read_text(encoding="utf-8"))  # JSON-Datei lesen → Liste mit Tickets

    for ticket in tickets:                                   # jedes Ticket nacheinander
        result = triage(ticket["text"])                      # Text an Claude → geprüftes Ergebnis
        print(f"{ticket['id']}: {result.category} | {result.priority} | {result.suggested_owner}")  # ID + Ergebnis ausgeben


if __name__ == "__main__":                                   # nur beim direkten Start ausführen
    main()