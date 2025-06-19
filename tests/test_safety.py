import pytest
from safety import SafetySystem

def test_no_emergency_on_normal_temp():
    """
    REQ-F04: Testet, dass bei normaler Temperatur kein Not-Aus ausgelöst wird.
    """
    safety = SafetySystem(max_temp=95.0)
    assert not safety.check(50.0)
    assert not safety.emergency_shutdown
    assert safety.last_error is None

def test_emergency_on_overtemperature():
    """
    REQ-F04: Testet, dass bei Übertemperatur ein Not-Aus ausgelöst wird.
    """
    safety = SafetySystem(max_temp=95.0)
    assert safety.check(100.0)
    assert safety.emergency_shutdown
    assert safety.last_error == "Übertemperatur"

def test_emergency_on_sensor_none():
    """
    REQ-F04: Testet, dass bei None als Sensorwert ein Not-Aus ausgelöst wird.
    """
    safety = SafetySystem()
    assert safety.check(None)
    assert safety.emergency_shutdown
    assert safety.last_error == "Sensorfehler"

def test_emergency_on_sensor_type_error():
    """
    REQ-F04: Testet, dass bei ungültigem Sensortyp ein Not-Aus ausgelöst wird.
    """
    safety = SafetySystem()
    assert safety.check("not_a_number")
    assert safety.emergency_shutdown
    assert safety.last_error == "Sensorfehler"

def test_reset_emergency():
    """
    REQ-F04: Testet das Zurücksetzen des Not-Aus-Zustands.
    """
    safety = SafetySystem()
    safety.check(100.0)
    safety.reset()
    assert not safety.emergency_shutdown
    assert safety.last_error is None