import pytest
import sys
import os

# Add project root to Python path, damit Imports im Test funktionieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
from gui import HeatingControlGUI

@pytest.fixture
def sensor():
    """
    Fixture für einen Temperatursensor mit Startwert 20.0°C.
    """
    return TemperatureSensor(initial_temp=20.0)

@pytest.fixture
def controller():
    """
    Fixture für einen Temperatur-Controller mit Sollwert 22.0°C.
    """
    return TemperatureController(target_temp=22.0)

@pytest.fixture
def burner():
    """
    Fixture für einen Brenner (ausgeschaltet).
    """
    return Burner()

@pytest.fixture
def gui(controller):
    """
    Fixture für die GUI, initialisiert mit dem Controller.
    """
    return HeatingControlGUI(controller)