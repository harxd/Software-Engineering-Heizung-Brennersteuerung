import pytest
from gui import HeatingControlGUI
from control import TemperatureController

@pytest.fixture
def gui():
    controller = TemperatureController(target_temp=22.0)
    return HeatingControlGUI(controller)

def test_temperature_display(gui):
    """REQ-F05: Test temperature display updates"""
    gui.update_current_temp(21.5)
    assert gui.current_temp_var.get() == "21.5°C"

def test_target_temperature_adjustment(gui):
    """REQ-F02: Test target temperature adjustment"""
    initial_temp = gui.controller.target_temperature
    
    gui.increase_temp()
    assert gui.controller.target_temperature == initial_temp + 0.5
    
    gui.decrease_temp()
    assert gui.controller.target_temperature == initial_temp

def test_burner_status_display(gui):
    """REQ-F05: Test burner status display"""
    gui.update_burner_status("ON")
    assert gui.burner_status_var.get() == "EIN"
    
    gui.update_burner_status("OFF")
    assert gui.burner_status_var.get() == "AUS"