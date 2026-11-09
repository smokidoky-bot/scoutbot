import pytest                                                    # Test-Werkzeug
from pydantic import ValidationError                             # der Fehler, den Pydantic bei falschen Werten wirft

from scoutbot.models import TriageResult                         # unser Formular


def test_valid_result_is_accepted():                             # Test 1: gültige Werte werden angenommen
    result = TriageResult(category="billing", priority="high", suggested_owner="billing-team")
    assert result.priority == "high"                             # prüfen: Wert ist korrekt gespeichert


def test_invalid_priority_is_rejected():                         # Test 2: falsche Priorität wird abgelehnt (verlangt)
    with pytest.raises(ValidationError):                         # erwartet: hier MUSS ein Fehler kommen
        TriageResult(category="billing", priority="urgent", suggested_owner="billing-team")   # „urgent“ ist nicht erlaubt


def test_extra_field_is_rejected():                              # Test 3: zusätzliche Felder werden abgelehnt
    with pytest.raises(ValidationError):
        TriageResult(category="billing", priority="low", suggested_owner="billing-team", mood="angry")   # „mood“ gibt es nicht