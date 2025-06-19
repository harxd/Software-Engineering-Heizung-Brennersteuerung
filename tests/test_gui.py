import pytest
from gui import HeatingControlGUI
from control import TemperatureController

class DummyPhotoImage:
    def __init__(self, *a, **kw): pass

class DummyLabel:
    def __init__(self, *a, **kw): pass
    def grid(self, *a, **kw): pass
    def configure(self, *a, **kw): pass
    def cget(self, *a, **kw): return ""

@pytest.fixture
def gui(monkeypatch):
    # Mock ImageTk.PhotoImage and tk.Label to avoid TclError in headless tests
    import gui as gui_module
    monkeypatch.setattr(gui_module, "ImageTk", type("ImageTk", (), {"PhotoImage": DummyPhotoImage}))
    import tkinter as tk_module
    monkeypatch.setattr(tk_module, "Label", DummyLabel)
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
    # Only check that method runs without error, since images and labels are mocked
    gui.update_burner_status("ON")
    gui.update_burner_status("OFF")