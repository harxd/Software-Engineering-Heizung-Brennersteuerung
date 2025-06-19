import pytest
from control import TemperatureController

# --- Dummy-Klassen für das Mocking von Tkinter und Pillow ---

class DummyStringVar:
    """Mock für tk.StringVar."""
    def __init__(self, master=None, value="", name=None):
        self._value = value
    def get(self):
        return self._value
    def set(self, value):
        self._value = value

class DummyPhotoImage:
    """Mock für ImageTk.PhotoImage."""
    def __init__(self, *args, **kwargs):
        pass

class DummyLabel:
    """Mock für tk.Label."""
    def __init__(self, *args, **kwargs):
        self._image = None
    def grid(self, *args, **kwargs):
        pass
    def configure(self, **kwargs):
        if "image" in kwargs:
            self._image = kwargs["image"]

class DummyTk:
    """Mock für tk.Tk."""
    def __init__(self, *args, **kwargs):
        self.tk = self
        self._last_child_ids = {}
        self._w = "."
        self.children = {}
        self._commands = {}
    def title(self, *args, **kwargs):
        pass
    def geometry(self, *args, **kwargs):
        pass
    def mainloop(self, *args, **kwargs):
        pass
    def call(self, *args, **kwargs):
        pass
    def createcommand(self, name, callback):
        self._commands[name] = callback

class DummyStyle:
    """Mock für ttk.Style."""
    def __init__(self, *args, **kwargs):
        pass
    def configure(self, *args, **kwargs):
        pass

# --- Pytest Fixture für gemockte GUI ---

@pytest.fixture
def gui(monkeypatch):
    """
    Fixture, die eine vollständig gemockte HeatingControlGUI zurückgibt.
    Alle relevanten Tkinter- und Pillow-Komponenten werden ersetzt.
    """
    import gui as gui_module
    import tkinter as tk_module
    import tkinter.ttk as ttk_module

    # Pillow-ImageTk Mock
    monkeypatch.setattr(gui_module, "ImageTk", type("ImageTk", (), {"PhotoImage": DummyPhotoImage}))
    # Tkinter-Komponenten Mock
    monkeypatch.setattr(tk_module, "Label", DummyLabel)
    monkeypatch.setattr(tk_module, "Tk", DummyTk)
    monkeypatch.setattr(tk_module, "StringVar", DummyStringVar)
    # ttk.Style Mock
    monkeypatch.setattr(ttk_module, "Style", DummyStyle)

    controller = TemperatureController(target_temp=21.0)
    return gui_module.HeatingControlGUI(controller)

# --- Tests für die GUI ---

def test_ist_temperatur_anzeige(gui):
    """
    Testet, ob die Ist-Temperatur korrekt angezeigt wird.
    """
    gui.update_current_temp(19.8)
    assert gui.current_temp_var.get() == "19.8°C"

def test_soll_temperatur_erhoehen_verringern(gui):
    """
    Testet das Erhöhen und Verringern der Soll-Temperatur über die GUI.
    """
    startwert = gui.controller.target_temperature
    gui.increase_temp()
    assert gui.controller.target_temperature == startwert + 0.5
    gui.decrease_temp()
    assert gui.controller.target_temperature == startwert

def test_soll_temperatur_anzeige(gui):
    """
    Testet, ob die Anzeige der Soll-Temperatur aktualisiert wird.
    """
    gui.controller.target_temperature = 23.5
    gui.update_target_temp_display()
    assert gui.target_temp_var.get() == "23.5°C"

def test_brenner_status_anzeige(gui):
    """
    Testet die Anzeige des Brennerstatus (ON/OFF).
    """
    gui.update_burner_status("ON")
    assert hasattr(gui, "current_burner_img")
    gui.update_burner_status("OFF")
    assert hasattr(gui, "current_burner_img")

def test_emergency_status_anzeige(gui):
    """
    Testet die Anzeige des Not-Aus-Status und der Fehlernachricht.
    """
    gui.update_emergency_status(True, error_msg="Sensorfehler")
    assert gui.error_var.get() == "Sensorfehler"
    gui.update_emergency_status(False)
    assert gui.error_var.get() == ""

def test_reset_emergency_ohne_safety(gui):
    """
    Testet, dass reset_emergency ohne Safety-Objekt keinen Fehler wirft.
    """
    gui.safety = None
    gui.reset_emergency()  # Sollte einfach durchlaufen

def test_reset_emergency_mit_safety(monkeypatch):
    """
    Testet, dass reset_emergency das SafetySystem zurücksetzt.
    """
    import gui as gui_module
    import tkinter as tk_module
    import tkinter.ttk as ttk_module

    # Dummy SafetySystem mit reset-Flag
    class DummySafety:
        def __init__(self):
            self.reset_called = False
        def reset(self):
            self.reset_called = True

    # Tkinter/Pillow/ttk Mocks
    monkeypatch.setattr(gui_module, "ImageTk", type("ImageTk", (), {"PhotoImage": DummyPhotoImage}))
    monkeypatch.setattr(tk_module, "Label", DummyLabel)
    monkeypatch.setattr(tk_module, "Tk", DummyTk)
    monkeypatch.setattr(tk_module, "StringVar", DummyStringVar)
    monkeypatch.setattr(ttk_module, "Style", DummyStyle)

    controller = TemperatureController(target_temp=20.0)
    safety = DummySafety()
    gui = gui_module.HeatingControlGUI(controller, safety=safety)
    gui.reset_emergency()