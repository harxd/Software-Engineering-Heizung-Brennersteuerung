from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
import time


def main():
    # Initialize components
    sensor = TemperatureSensor(initial_temp=18.0)  # Initial temperature
    controller = TemperatureController(target_temp=22.0)  # Target temperature
    burner = Burner()

    print("Heizung – Brennersteuerung Simulation")
    print("-" * 40)

    # Main simulation loop
    while True:
        # Get current measured temperature
        current_temp = sensor.get_temperature()

        # Determine if the burner needs to be switched ON/OFF
        if controller.check_temperature(current_temp):
            burner.switch_on()
        else:
            burner.switch_off()

        # Display status on the console
        print(f"Ist-Temperatur: {current_temp}°C | Soll-Temperatur: {controller.target_temperature}°C | "
              f"Brenner: {burner.status()}")

        # Wait for a bit before the next measurement (simulate real-time system)
        time.sleep(1)


if __name__ == "__main__":
    main()