import pytest
from burner import Burner

def test_initial_burner_state():
    """
    REQ-F03: Testet den Anfangszustand des Brenners.
    """
    burner = Burner()
    assert burner.is_on is False
    assert burner.status() == "OFF"

def test_burner_switching():
    """
    REQ-F03: Testet das Ein- und Ausschalten des Brenners.
    """
    burner = Burner()

    burner.switch_on()
    assert burner.is_on is True
    assert burner.status() == "ON"

    burner.switch_off()
    assert burner.is_on is False
    assert burner.status() == "OFF"