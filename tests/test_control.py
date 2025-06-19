import pytest
from control import TemperatureController

def test_target_temperature_setting():
    """
    REQ-F02: Testet das Setzen der Soll-Temperatur.
    """
    controller = TemperatureController(target_temp=22.0)
    assert controller.target_temperature == 22.0

def test_burner_control_logic():
    """
    REQ-F03: Testet die Steuerlogik für das automatische Schalten des Brenners.
    """
    controller = TemperatureController(target_temp=22.0)
    
    # Test: Temperatur unter Sollwert
    assert controller.check_temperature(21.0) is True  # Brenner AN
    
    # Test: Temperatur gleich Sollwert
    assert controller.check_temperature(22.0) is False  # Brenner AUS
    
    # Test: Temperatur über Sollwert
    assert controller.check_temperature(23.0) is False  # Brenner AUS