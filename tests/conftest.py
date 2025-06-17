import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
from gui import HeatingControlGUI

@pytest.fixture
def sensor():
    return TemperatureSensor(initial_temp=20.0)

@pytest.fixture
def controller():
    return TemperatureController(target_temp=22.0)

@pytest.fixture
def burner():
    return Burner()

@pytest.fixture
def gui(controller):
    return HeatingControlGUI(controller)