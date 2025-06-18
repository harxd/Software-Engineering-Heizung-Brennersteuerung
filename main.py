from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
from gui import HeatingControlGUI
from safety import SafetySystem
import time
import threading


def update_gui(gui, sensor, controller, burner, safety):
    """Update GUI with current system status"""
    while True:
        current_temp = sensor.get_temperature(burner.is_on)

        # Safety-Check
        if safety.check(current_temp):
            burner.switch_off()
            gui.update_emergency_status(True, safety.last_error)
        else:
            gui.update_emergency_status(False)
            if controller.check_temperature(current_temp):
                burner.switch_on()
            else:
                burner.switch_off()

        # Update GUI elements
        gui.update_current_temp(current_temp)
        gui.update_burner_status(burner.status())
        
        time.sleep(0.1)


def main():
    # Initialize components
    sensor = TemperatureSensor(initial_temp=15.0)
    controller = TemperatureController(target_temp=22.0)
    burner = Burner()
    safety = SafetySystem(max_temp=95.0)
    
    # Create and setup GUI (safety als Referenz übergeben)
    gui = HeatingControlGUI(controller, safety=safety)
    
    # Start update thread
    update_thread = threading.Thread(target=update_gui, 
                                   args=(gui, sensor, controller, burner, safety),
                                   daemon=True)
    update_thread.start()
    
    # Start GUI main loop
    gui.start()


if __name__ == "__main__":
    main()