import logging
from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
from gui import HeatingControlGUI
from safety import SafetySystem
import time
import threading

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Heizung")


def update_gui(gui, sensor, controller, burner, safety):
    """
    Aktualisiert die GUI mit dem aktuellen Systemstatus.
    Führt die Temperaturmessung, Sicherheitsprüfung und Brennersteuerung durch.
    """
    last_burner_status = burner.status()
    last_emergency = False
    while True:
        current_temp = sensor.get_temperature(burner.is_on)

        # Sicherheitsprüfung
        if safety.check(current_temp):
            if not last_emergency:
                logger.warning(f"EMERGENCY: {safety.last_error}")
                last_emergency = True
            burner.switch_off()
            gui.update_emergency_status(True, safety.last_error)
        else:
            if last_emergency:
                logger.info("Emergency cleared or reset.")
                last_emergency = False
            gui.update_emergency_status(False)
            if controller.check_temperature(current_temp):
                burner.switch_on()
            else:
                burner.switch_off()

        # Brennerstatus-Änderung protokollieren
        current_burner_status = burner.status()
        if current_burner_status != last_burner_status:
            logger.info(
                f"Burner switched {'ON' if current_burner_status == 'ON' else 'OFF'}"
            )
            last_burner_status = current_burner_status

        # GUI-Elemente aktualisieren
        gui.update_current_temp(current_temp)
        gui.update_burner_status(burner.status())

        time.sleep(0.1)


def main():
    """
    Initialisiert alle Komponenten und startet die Anwendung.
    """
    # Komponenten initialisieren
    sensor = TemperatureSensor(initial_temp=15.0)
    controller = TemperatureController(target_temp=22.0)
    burner = Burner()
    safety = SafetySystem(max_temp=95.0)

    # GUI erstellen (safety als Referenz übergeben)
    gui = HeatingControlGUI(controller, safety=safety)

    # Update-Thread starten
    update_thread = threading.Thread(
        target=update_gui,
        args=(gui, sensor, controller, burner, safety),
        daemon=True
    )
    update_thread.start()

    # GUI-Hauptloop starten
    gui.start()


if __name__ == "__main__":
    main()