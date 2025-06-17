import pytest
from control import TemperatureController

def test_target_temperature_setting():
    """REQ-F02: Test target temperature setting"""
    controller = TemperatureController(target_temp=22.0)
    assert controller.target_temperature == 22.0

def test_burner_control_logic():
    """REQ-F03: Test automated burner control logic"""
    controller = TemperatureController(target_temp=22.0)
    
    # Test below target temperature
    assert controller.check_temperature(21.0) == True  # Should turn ON
    
    # Test at target temperature
    assert controller.check_temperature(22.0) == False  # Should turn OFF
    
    # Test above target temperature
    assert controller.check_temperature(23.0) == False  # Should turn OFF