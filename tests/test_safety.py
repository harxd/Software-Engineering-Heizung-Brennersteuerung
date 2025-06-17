import pytest
from safety import SafetySystem

def test_no_emergency_on_normal_temp():
    safety = SafetySystem(max_temp=95.0)
    assert not safety.check(50.0)
    assert not safety.emergency_shutdown
    assert safety.last_error is None

def test_emergency_on_overtemperature():
    safety = SafetySystem(max_temp=95.0)
    assert safety.check(100.0)
    assert safety.emergency_shutdown
    assert safety.last_error == "Übertemperatur"

def test_emergency_on_sensor_none():
    safety = SafetySystem()
    assert safety.check(None)
    assert safety.emergency_shutdown
    assert safety.last_error == "Sensorfehler"

def test_emergency_on_sensor_type_error():
    safety = SafetySystem()
    assert safety.check("not_a_number")
    assert safety.emergency_shutdown
    assert safety.last_error == "Sensorfehler"

def test_reset_emergency():
    safety = SafetySystem()
    safety.check(100.0)
    safety.reset()
    assert not safety.emergency_shutdown
    assert safety.last_error is None