from scoutbot.customers import find_customer                  # die Kartei-Suche aus Schritt 4


def test_known_customer_is_found():                           # Test 1: vorhandener Kunde wird gefunden
    customer = find_customer("C-001")                         # Lena suchen
    assert customer is not None                               # es muss etwas gefunden werden
    assert customer.first_name == "Lena"                      # und zwar die richtige Person


def test_unknown_customer_returns_none():                     # Test 2: unbekannte Nummer → None statt Absturz
    assert find_customer("C-999") is None                     # C-999 gibt es nicht