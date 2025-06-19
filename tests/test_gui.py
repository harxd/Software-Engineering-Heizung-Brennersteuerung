import pytest
from gui import HeatingControlGUI
from control import TemperatureController

class DummyPhotoImage:
    """
    Dummy-Klasse zum Mocken von ImageTk.PhotoImage für GUI-Tests ohne echte Bilder.
    """
    def __init__(self, *a, **kw):
        pass

class DummyLabel:
    """
    Dummy-Klasse zum Mocken von tk.Label für GUI-Tests ohne echte Widgets.
    """
    def __init__(self, *a, **kw):
        pass
    def grid(self, *a, **kw):
        pass
    def configure(self, *a, **kw):
        pass
    def cget(self, *a, **kw):
        return ""

@pytest.fixture
def gui(monkeypatch):
    """
    Fixture für eine gemockte GUI, die keine echten Images oder Labels benötigt.
    Verhindert Fehler in headless-Testumgebungen.
    """
    import gui as gui_module
    monkeypatch.setattr(gui_module, "ImageTk", type("ImageTk", (), {"PhotoImage": DummyPhotoImage}))
    import tkinter as tk_module
    monkeypatch.setattr(tk_module, "Label", DummyLabel)
    controller = TemperatureController(target_temp=22.0)
    return HeatingControlGUI(controller)

def test_temperature_display(gui):
    """
    REQ-F05: Testet, ob die Temperaturanzeige korrekt aktualisiert wird.
    """
    gui.update_current_temp(21.5)
    assert gui.current_temp_var.get() == "21.5°C"

def test_target_temperature_adjustment(gui):
    """
    REQ-F02: Testet die Anpassung der Soll-Temperatur über die GUI.
    """
    initial_temp = gui.controller.target_temperature

    gui.increase_temp()
    assert gui.controller.target_temperature == initial_temp + 0.5

    gui.decrease_temp()
    assert gui.controller.target_temperature == initial_temp

def test_burner_status_display(gui):
    """
    REQ-F05: Testet die Anzeige des Brennerstatus in der GUI.
    """
    # Nur prüfen, dass die Methode ohne Fehler läuft, da Images/Labels gemockt sind
    gui.update_burner_status("ON")
    gui.update_burner_status("OFF")