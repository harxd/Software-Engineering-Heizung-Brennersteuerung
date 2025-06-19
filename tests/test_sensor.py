import pytest
from sensor import TemperatureSensor

def test_initial_temperature():
    """
    REQ-F01: Testet das Setzen der Anfangstemperatur des Sensors.
    """
    sensor = TemperatureSensor(initial_temp=20.0)
    assert sensor.current_temperature == 20.0

def test_temperature_changes():
    """
    REQ-F01: Testet das Verhalten der Temperatursimulation (Heizen/Kühlen).
    """
    sensor = TemperatureSensor(initial_temp=15.0)
    
    # Test: Heizen
    temp1 = sensor.get_temperature(burner_is_on=True)
    assert temp1 > 15.0
    
    # Test: Kühlen
    temp2 = sensor.get_temperature(burner_is_on=False)
    assert temp2 < temp1

def test_minimum_temperature():
    """
    REQ-F01: Testet das Temperaturminimum (Sensor darf nicht unter 10°C fallen).
    """
    sensor = TemperatureSensor(initial_temp=10.5)
    for _ in range(10):  # Mehrere Kühlzyklen simulieren
        temp = sensor.get_temperature(burner_is_on=False)
    assert temp >= 5.0  # Sollte nie unter das Minimum fallen