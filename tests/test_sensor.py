import pytest
from sensor import TemperatureSensor

def test_initial_temperature():
    """REQ-F01: Test initial temperature setting"""
    sensor = TemperatureSensor(initial_temp=20.0)
    assert sensor.current_temperature == 20.0

def test_temperature_changes():
    """REQ-F01: Test temperature simulation behavior"""
    sensor = TemperatureSensor(initial_temp=15.0)
    
    # Test heating
    temp1 = sensor.get_temperature(burner_is_on=True)
    assert temp1 > 15.0
    
    # Test cooling
    temp2 = sensor.get_temperature(burner_is_on=False)
    assert temp2 < temp1

def test_minimum_temperature():
    """REQ-F01: Test minimum temperature limit"""
    sensor = TemperatureSensor(initial_temp=10.5)
    for _ in range(10):  # Run multiple cooling cycles
        temp = sensor.get_temperature(burner_is_on=False)
    assert temp >= 10.0  # Should never go below minimum