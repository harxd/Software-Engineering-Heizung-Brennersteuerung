import pytest
from burner import Burner

def test_initial_burner_state():
    """REQ-F03: Test initial burner state"""
    burner = Burner()
    assert burner.is_on == False
    assert burner.status() == "OFF"

def test_burner_switching():
    """REQ-F03: Test burner switching functionality"""
    burner = Burner()
    
    burner.switch_on()
    assert burner.is_on == True
    assert burner.status() == "ON"
    
    burner.switch_off()
    assert burner.is_on == False
    assert burner.status() == "OFF"